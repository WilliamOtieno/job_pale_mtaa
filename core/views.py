from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, JobForm
from .models import *


# Create your views here.

def index(request):
    return render(request, "home.html", )


def aboutPage(request):
    return render(request, "about.html", )


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:login')
    context = {
        'form': form,
    }
    return render(request, "register.html", context=context)


def placements(request):
    customer = Customer.objects.get(user=request.user)
    placements = Job.objects.all().filter(customer=customer)
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
        'job_form': job_form,
    }
    return render(request, "placements.html", context=context)


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
