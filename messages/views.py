from django.contrib.auth import get_user_model, get_user
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ChatForm, ReplyForm
from .models import Chat
from .signals import chat_view_handler
from .shortcuts import is_similar_objects as is_similar_user

TEMPLATE_URL = 'messages'

User = get_user_model()


def read_chat(request, id, user=None):
    template_name = f'{TEMPLATE_URL}/read_chat.html'
    if user is None:
        user = request.user.username
    chat = get_object_or_404(Chat, id=id, starter__username__iexact=user)
    # Prevent access to authorised participants
    participants = list((chat.starter, chat.recipient))
    if request.user not in participants:
        raise PermissionDenied
    # Call built in signals to start their work
    chat_view_handler.send(sender=Chat, request=request.user, obj=chat)
    replies = chat.replies.all()
    return render(request, template_name, context={
        'chat': chat,
        'replies': replies
    })


def list_chats(request):
    template_name = f'{TEMPLATE_URL}/list_chats.html'
    active_chats = Chat.objects.filter(
        Q(starter=request.user) |
        Q(recipient=request.user, status__in=[Chat.STATUS_ACTIVE, Chat.STATUS_NEW]))
    newest_chats = Chat.objects.filter(
        Q(recipient=request.user, status=Chat.STATUS_ACTIVE_AND_NEW) |
        Q(status=Chat.STATUS_NEW)).exclude(
        replies__user=request.user)
    return render(request, template_name, context={
        'chats': active_chats,
        'newest_chats': newest_chats,
    })


def start_chat(request, user):
    template_name = f'{TEMPLATE_URL}/start_chat.html'
    current_user = get_user(request)
    recipient = get_object_or_404(User, username=user)
    recipient_received_chats = recipient.chats_received.filter(starter=current_user)
    current_user_received_chats = current_user.chats_started.filter(recipient=recipient)
    is_same_recipient = is_similar_user(current_user, recipient)
    form_kwargs = {'is_same_recipient': is_same_recipient}
    try:
        chat = current_user_received_chats.exists() or recipient_received_chats.exists()
        chat_obj = recipient_received_chats.get()
        is_exists = True
        form = ReplyForm
    except Chat.DoesNotExist:
        chat_obj = None
        is_exists = False
        form = ChatForm
    finally:
        if request.method == 'POST':
            form = form(data=request.POST, **form_kwargs)
            if form.is_valid():
                n = form.save(commit=False)
                if is_exists:
                    print('About to save reply')
                    n.user = current_user
                    n.message = chat_obj
                else:
                    n.starter = current_user
                    n.recipient = recipient
                n.save()
                return redirect(n.get_absolute_url())
        else:
            form = form(**form_kwargs)
        context = {
            'form': form,
            'is_exists': is_exists,
            'is_same_recipient': is_same_recipient,
            'recipient': recipient,
        }
    # Strictly for debugging purpose!
    print('We are using', form.__class__.__name__)
    return render(request, template_name, context=context)
