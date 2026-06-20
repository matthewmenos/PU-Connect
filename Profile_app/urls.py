from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('complete/', views.complete_profile, name='complete_profile'),
    path('api/me/', views.get_my_profile, name='get_my_profile'),
    path('api/update/', views.update_profile_api, name='update_profile'),
]

