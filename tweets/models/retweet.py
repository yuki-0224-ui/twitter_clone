from django.db import models
from django.conf import settings


class Retweet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='retweets'
    )
    tweet = models.ForeignKey(
        'Tweet',
        on_delete=models.CASCADE,
        related_name='retweets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tweet')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} retweeted {self.tweet.id}'
