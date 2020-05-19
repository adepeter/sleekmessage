from django.apps import AppConfig


class MessagesConfig(AppConfig):
    name = 'messages'
    label = 'chats'
    
    def ready(self):
        from . import signals
