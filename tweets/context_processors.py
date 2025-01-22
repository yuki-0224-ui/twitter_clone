from tweets.models import Notification


def notification_context(request):
    context = {
        'unread_notifications_count': 0
    }

    if hasattr(request, 'user') and request.user.is_authenticated:
        context['unread_notifications_count'] = (
            Notification.objects
            .filter(recipient=request.user, is_read=False)
            .count()
        )

    return context
