from django.db import models
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    tweet = models.ForeignKey(
        'Tweet',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} commented on {self.tweet.id}'
