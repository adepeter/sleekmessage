from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal

from .models import Chat, Reply

chat_view_handler = Signal(providing_args=(['request']))


@receiver(post_save, sender=Chat)
def chat_views(sender, instance, created, **kwargs):
    if created:
        instance.chat_views.create(user=instance.starter)


@receiver(post_save, sender=Reply)
def update_chat_is_replied(sender, instance, created, **kwargs):
    if created:
        instance.message.is_replied = True
        instance.message.status = Chat.STATUS_NEW
        instance.message.save()


@receiver(chat_view_handler)
def view_handler(sender, request, obj, **kwargs):
    cv = [chat_view.user for chat_view in obj.chat_views.all()]
    if not request in cv:
        obj.chat_views.create(user=request)
        obj.status = Chat.STATUS_ACTIVE
        obj.save()
    else:
        if obj.status == 0:
            obj.status = Chat.STATUS_ACTIVE
            obj.save()
