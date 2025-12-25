from .models import Message

def unread_message_count(request):
    if request.user.is_authenticated:
        return {
            "unread_count": Message.objects.filter(
                receiver=request.user,
                is_read=False
            ).count()
        }
    return {}