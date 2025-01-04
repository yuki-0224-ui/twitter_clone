from django.db import models
from django.conf import settings


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    tweet = models.ForeignKey(
        'Tweet',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tweet')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} likes {self.tweet.id}'
