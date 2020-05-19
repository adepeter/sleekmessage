from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

User = get_user_model()


class ChatManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            latest_replies=models.Count('replies__created')
        ).order_by('-modified', '-latest_replies')


class Chat(models.Model):
    STATUS_NEW = 0
    STATUS_ACTIVE = 1
    STATUS_ACTIVE_AND_NEW = 2

    STATUS_CHOICES = (
        (STATUS_NEW, _('New')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_ACTIVE_AND_NEW, _('Active and New')),
    )

    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_started')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_received')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    time_sent = models.DateTimeField(default=timezone.now)
    is_replied = models.BooleanField(verbose_name=_('Chat replied?'), default=False)
    status = models.PositiveSmallIntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES,
                                              default=STATUS_ACTIVE_AND_NEW)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = ChatManager()

    def get_absolute_url(self):
        kwargs = {
            'id': self.id,
            'user': self.starter.username
        }
        return reverse('read_chat', kwargs=kwargs)

    def __str__(self):
        return 'Correspondence started between %(starter)s and %(recipient)s' % {'starter': self.starter,
                                                                                 'recipient': self.recipient}


class Reply(models.Model):
    message = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    time_replied = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'replies'

    def get_absolute_url(self):
        kwargs = {'id': self.message.id}
        if self.message.recipient == self.user:
            kwargs.update({'starter': self.user})
        return reverse('read_chat', kwargs=kwargs)

    def __str__(self):
        return f'{self.user} reply to {self.message}'


class ChatView(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_views')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} viewed {self.chat}'
