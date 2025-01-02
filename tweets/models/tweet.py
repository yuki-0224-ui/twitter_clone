from django.db import models
from django.conf import settings


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'

    @classmethod
    def get_timeline_for_user(cls):
        return cls.objects.select_related('user').all()

    @classmethod
    def get_following_timeline_for_user(cls, user):
        if not user:
            return cls.objects.none()

        following_users = user.following.values_list('followee', flat=True)
        return cls.objects.select_related('user').filter(user_id__in=following_users)

    @classmethod
    def get_user_timeline(cls, user):
        return cls.objects.filter(user=user).select_related('user')

    @classmethod
    def get_liked_by(cls, user):
        return cls.objects.filter(likes__user=user).select_related('user')

    @classmethod
    def get_retweeted_by(cls, user):
        return cls.objects.filter(retweets__user=user).select_related('user')

    @classmethod
    def get_commented_by(cls, user):
        return cls.objects.filter(comments__user=user).select_related('user')
