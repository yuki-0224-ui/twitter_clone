from django.db import models
from django.conf import settings
from django.db.models import Count, Q, OuterRef, Exists
from django.db.models.functions import Coalesce


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
    def with_interaction_details(cls, user):
        if not user or not user.is_authenticated:
            return cls.objects.none()

        # 集計に影響を与えないために、サブクエリを使って取得
        from tweets.models import Retweet, Follow
        latest_retweet = models.Subquery(
            Retweet.objects.filter(
                tweet=OuterRef('pk')
            ).order_by('-created_at').values('created_at')[:1]
        )

        following_exists = Exists(
            Follow.objects.filter(
                follower=user,
                followee=OuterRef('user')
            )
        )

        return cls.objects.select_related('user').annotate(
            likes_count=Count('likes', distinct=True),
            liked_by_user=Count(
                'likes',
                filter=Q(likes__user=user),
                distinct=True
            ),
            retweets_count=Count(
                'retweets',
                distinct=True
            ),
            retweeted_by_user=Count(
                'retweets',
                filter=Q(retweets__user=user),
                distinct=True
            ),
            is_following=following_exists,
            last_retweet_at=latest_retweet,
            effective_date=Coalesce('last_retweet_at', 'created_at')
        ).order_by('-effective_date', '-created_at')

    @classmethod
    def get_timeline_for_user(cls, user):
        return cls.with_interaction_details(user)

    @classmethod
    def get_following_timeline_for_user(cls, user):
        following_users = user.following.values_list('followee', flat=True)
        return cls.with_interaction_details(user).filter(user_id__in=following_users)
