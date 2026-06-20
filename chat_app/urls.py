from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat, name='chat'),
    path('api/conversations/', views.get_conversations, name='get_conversations'),
    path('api/messages/<int:conv_id>/', views.get_messages, name='get_messages'),
    path('api/start/', views.start_conversation, name='start_conversation'),
<<<<<<< HEAD
    path('api/start-direct/', views.start_direct, name='start_direct'),
    path('api/push-subscribe/', views.push_subscribe, name='push_subscribe'),
    path('api/push-unsubscribe/', views.push_unsubscribe, name='push_unsubscribe'),
=======
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/read-all/', views.mark_notifications_read, name='mark_notifications_read'),
    path('api/push-subscription/', views.save_push_subscription, name='save_push_subscription'),
    path('api/vapid-public-key/', views.get_vapid_public_key, name='get_vapid_public_key'),
>>>>>>> deb2760f18d5604cf91abcb458a7f3c989188b88
]
