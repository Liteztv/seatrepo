from django import template

register = template.Library()

@register.simple_tag
def unread_messages(user):
    if not user.is_authenticated:
        return 0
    return user.received_messages.filter(is_read=False).count()

@register.filter
def other_user(conversation, user):
    return conversation.get_other_user(user)


@register.filter
def endswith(value, suffix):
    try:
        return str(value).endswith(str(suffix))
    except:
        return False
