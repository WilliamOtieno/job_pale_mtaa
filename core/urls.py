from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),

    path('', views.index, name='home'),
    path('login/', views.loginPage, name='login'),
    path('about/', views.aboutPage, name='about'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('placements/', views.placements, name='placements'),
    path('placements/<id>/', views.placement_detail, name='placement-detail'),
    path('bill/<id>/', views.invoice_view, name='invoice-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
