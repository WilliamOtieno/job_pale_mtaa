from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.loginPage, name='login'),
    path('about/', views.aboutPage, name='about'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('placements/', views.placements, name='placements'),
    path('placements/<id>/', views.placement_detail, name='placement-detail'),
]