from django.contrib import admin
from .models import Customer, Worker, Job, Bill

"""
This file simply catches our models from the models.py file and registers them in an admin dashboard so that one can 
inspect all the data persisting the platform.
"""

admin.site.register(Worker)
admin.site.register(Customer)
admin.site.register(Job)
admin.site.register(Bill)
