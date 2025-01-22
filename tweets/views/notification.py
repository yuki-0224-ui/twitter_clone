from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from tweets.models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related(
            'actor',
            'tweet__user'
        )

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

        return super().get(request, *args, **kwargs)


notification_list = NotificationListView.as_view()
