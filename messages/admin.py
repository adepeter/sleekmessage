from django.contrib import admin
from .models import Chat, ChatView, Reply


# Register your models here.

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'starter', 'recipient', 'is_replied', 'time_sent', 'created', 'modified']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'time_replied', 'created', 'modified']


@admin.register(ChatView)
class ChatViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat', 'created']
