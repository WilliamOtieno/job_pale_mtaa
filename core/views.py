import threading

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import CustomRegisterForm, JobForm
from .models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


generate_token = TokenGenerator()


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(request, user):
    current_site = get_current_site(request)
    subject = "Activate Your Account"
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }
    email_body = render_to_string(
        template_name="mail_body.html", context=context)
    email = EmailMultiAlternatives(subject=subject, body=email_body,
                                   from_email='Fix It <accounts@fixit.com>',
                                   to=[user.email])
    email.attach_alternative(content=email_body, mimetype="text/html")
    EmailThread(email).start()


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
        print(e)
    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             "Your email was successfully verified!")
        return redirect('login')

    return redirect('app:home')


# Create your views here.

def index(request):
    return render(request, "home.html", )


def aboutPage(request):
    return render(request, "about.html", )


def registerPage(request):
    form = CustomRegisterForm()
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        print(request)
        if form.is_valid():
            form.save()
            user = User.objects.get(email=request.POST["email"])
            user.is_active = False
            send_activation_email(request=request, user=user)
            return redirect('app:login')

    context = {
        'form': form,
    }
    return render(request, "register.html", context=context)


@login_required
def placements(request):
    customer = Customer.objects.get(user=request.user)
    placements = Job.objects.all().filter(customer=customer)
    bills = Bill.objects.all().filter(job__customer=customer)
    job_form = JobForm()
    if request.method == 'POST':
        job_form = JobForm(request.POST, request.FILES)
        if job_form.is_valid():
            job_data = job_form.save(commit=False)
            job_data.customer = customer
            job_data.save()
            return redirect('app:placements')

    context = {
        'placements': placements,
        'bills': bills,
        'job_form': job_form,
    }
    return render(request, "placements.html", context=context)


@login_required
def placement_detail(request, id):
    specific_placement = Job.objects.get(id=id)
    context = {
        'placement': specific_placement,
    }
    return render(request, "placement_detail.html", context=context)


@login_required
def dashboard(request):
    total_workers = Worker.objects.count()
    total_users = User.objects.count()
    total_requests = Job.objects.count()
    context = {
        'total_workers': total_workers,
        'total_users': total_users,
        'total_requests': total_requests,
    }
    return render(request, "dashboard.html", context=context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:dashboard')
        else:
            return redirect('app:login')
    context = {}
    return render(request, "login.html", context=context)


def logoutPage(request):
    logout(request)
    return redirect('app:login')


@login_required
def invoice_view(request, id):
    bill = Bill.objects.get(id=id)
    context = {
        'bill': bill
    }
    return render(request, "invoice.html", context=context)
