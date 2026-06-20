from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Message, Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


def _send_web_push(user, title, body, url='/chat/'):
    """Send a Web Push notification to all of a user's subscribed devices."""
    from .models import PushSubscription
    subs = PushSubscription.objects.filter(user=user)
    if not subs.exists():
        return
    vapid_private = getattr(settings, 'VAPID_PRIVATE_KEY', '')
    vapid_email   = getattr(settings, 'VAPID_CLAIMS_EMAIL', '')
    if not vapid_private or not vapid_email:
        return
    try:
        from pywebpush import webpush, WebPushException
    except ImportError:
        return
    payload = json.dumps({'title': title, 'body': body, 'url': url, 'icon': '/static/icons/icon-192.png', 'badge': '/static/icons/icon-192.png'})
    for sub in subs:
        try:
            webpush(
                subscription_info={'endpoint': sub.endpoint, 'keys': {'p256dh': sub.p256dh, 'auth': sub.auth}},
                data=payload,
                vapid_private_key=vapid_private,  # PEM string decoded from settings
                vapid_claims={'sub': f'mailto:{vapid_email}'},
                content_encoding='aes128gcm',
            )
        except Exception:
            pass


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        # Get the recipient (the other person in the conversation)
        recipient = instance.conversation.participants.exclude(id=instance.sender.id).first()

        if recipient:
            preview = (instance.text[:50] + '...') if instance.text and len(instance.text) > 50 else instance.text or 'Sent an attachment'

            # Create the database notification
            notification = Notification.objects.create(
                user=recipient,
                type='message',
                title=f"New Message from {instance.sender.username}",
                content=preview,
                link='/chat/',
            )

            # Web Push to the recipient's devices
            _send_web_push(
                user=recipient,
                title=f"New message from {instance.sender.get_full_name() or instance.sender.username}",
                body=preview,
                url='/chat/',
            )

            # Trigger real-time push via Channels
            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f"user_{recipient.id}",
                    {
                        "type": "notification_message",
                        "data": {
                            "id": notification.id,
                            "type": "message",
                            "title": notification.title,
                            "content": notification.content,
                            "created_at": notification.created_at.strftime("%H:%M"),
                        }
                    }
                )
            
            # Send Web Push notification (for mobile/closed app notifications)
            try:
                from .utils import send_web_push
                send_web_push(
                    user=recipient,
                    title=notification.title,
                    message=notification.content,
                    link=notification.link
                )
            except Exception as e:
                print(f"Error triggering send_web_push: {e}")
