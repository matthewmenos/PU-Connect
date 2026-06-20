from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
<<<<<<< HEAD
    path('', views.dashboard, name='dashboard'),
    path('services/', views.dashboard_services, name='dashboard_services'),
    path('products/', views.dashboard_products, name='dashboard_products'),
=======
    path('dashboard/', views.dashboard, name='dashboard'),
>>>>>>> deb2760f18d5604cf91abcb458a7f3c989188b88
]