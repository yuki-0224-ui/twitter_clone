from django.db import models
from django.conf import settings
from django.db.models import Count, Q


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=140, blank=True, null=True)
    image = models.ImageField(
        upload_to='tweet_images/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        text = f'{self.user.username}: '
        if self.content and self.image:
            return text + f'{self.content[:30]} [画像付き]'
        elif self.content:
            return text + self.content[:30]
        elif self.image:
            return text + '[画像のみの投稿]'
        return text + '[投稿なし]'

    @classmethod
    def with_like_details(cls, user):
        if not user or not user.is_authenticated:
            return cls.objects.none()

        return cls.objects.select_related('user').annotate(
            likes_count=Count('likes', distinct=True),
            liked_by_user=Count('likes', filter=Q(likes__user=user))
        ).order_by('-created_at')

    @classmethod
    def get_timeline_for_user(cls, user):
        return cls.with_like_details(user)

    @classmethod
    def get_following_timeline_for_user(cls, user):
        following_users = user.following.values_list('followee', flat=True)
        return cls.with_like_details(user).filter(user_id__in=following_users)
