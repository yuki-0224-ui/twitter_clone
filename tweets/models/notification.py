from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError


class Notification(models.Model):
    LIKE = 'like'
    RETWEET = 'retweet'
    COMMENT = 'comment'

    NOTIFICATION_TYPES = [
        (LIKE, 'いいね'),
        (RETWEET, 'リツイート'),
        (COMMENT, 'コメント'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_received'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_created'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )
    tweet = models.ForeignKey(
        'Tweet',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def create_notification(cls, recipient, actor, notification_type, tweet=None):
        try:
            notification = cls.objects.create(
                recipient=recipient,
                actor=actor,
                notification_type=notification_type,
                tweet=tweet
            )
            subject = f'{notification.notification_type}の新しい通知があります'
            html_message = render_to_string('emails/notification.html', {
                'notification': notification,
                'recipient': recipient,
            })
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
                html_message=html_message,
                fail_silently=True
            )
            return notification
        except Exception as e:
            raise ValidationError(f"通知の作成に失敗しました: {str(e)}")
