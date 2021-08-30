from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
"""
This file will define our models which act as a representation of our database tables. Ergo, each class represents 
the table in our database; Worker, Customer, Job

The Worker will be added directly to the system by the admin of the platform

The Customer will be a user of the system hence there is a one to one relationship between a user and a customer;
this simply means that each user of the system can be a customer requesting for a service.

The Job will have a relationship to a customer requesting the service and the Worker who will execute the service
The Job will also have an image field where the customer will upload images concerning the problem...we just rescale
the image so as not to overload our file system with very large media files
"""


class Worker(models.Model):
    name = models.CharField(default='', max_length=20)
    email = models.EmailField(default='')
    phone = models.CharField(default='', max_length=15)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"


class Job(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    title = models.CharField(default='', max_length=100)
    location = models.CharField(default='', max_length=100)
    description = models.TextField(default='')
    picture = models.ImageField(null=True, upload_to='job_pics/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.customer}"


class Bill(models.Model):
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE)
    narrative = models.CharField(default='', max_length=500)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=18)
    cleared = models.BooleanField(default=False, verbose_name='Cleared')
    date_incurred = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KES. {self.total}"
