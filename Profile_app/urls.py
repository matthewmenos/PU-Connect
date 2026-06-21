from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('complete/', views.complete_profile, name='complete_profile'),
    path('api/me/', views.get_my_profile, name='get_my_profile'),
    path('api/update/', views.update_profile_api, name='update_profile'),
    path('api/user/<str:username>/', views.public_profile_api, name='public_profile_api'),
    path('api/follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('api/report/<str:username>/', views.report_user, name='report_user'),
    path('<str:username>/', views.public_profile_page, name='public_profile'),
]

