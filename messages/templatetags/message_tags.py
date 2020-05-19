from django import template

from ..models import Reply

register = template.Library()


@register.simple_tag
def typeofinstance(obj):
    r = Reply.objects.filter(message=obj).latest('created')
    # r = obj.replies.latest('created')
    return r
