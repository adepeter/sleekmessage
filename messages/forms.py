from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Chat, Reply


class BaseMessageForm(forms.ModelForm):
    class Meta:
        model = None
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.is_same_recipient = kwargs.pop('is_same_recipient', None)
        super().__init__(*args, **kwargs)



class ChatForm(BaseMessageForm):
    class Meta(BaseMessageForm.Meta):
        model = Chat

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_same_recipient:
            self.fields['text'].widget.attrs.update({'disabled': True})


class ReplyForm(BaseMessageForm):
    class Meta(BaseMessageForm.Meta):
        model = Reply

    def __init__(self, *args, **kwargs):
        if kwargs.get('is_same_recipient'):
            del kwargs['is_same_recipient']
        super().__init__(*args, **kwargs)