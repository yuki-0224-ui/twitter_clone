from django.db import models
from django.conf import settings


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('follower', 'followee')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F('followee')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f'{self.follower.username} follows {self.followee.username}'
