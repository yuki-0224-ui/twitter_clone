from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tweets.models import Follow

User = get_user_model()


@login_required
def follow_user(request, username):
    if request.method != 'POST':
        return redirect('tweets:home')

    user_to_follow = get_object_or_404(User, username=username)
    follow_relationship = Follow.objects.filter(
        follower=request.user,
        followee=user_to_follow
    )

    if follow_relationship.exists():
        follow_relationship.delete()
        messages.success(
            request, f'@{user_to_follow.username}のフォローを解除しました')
    else:
        Follow.objects.create(
            follower=request.user,
            followee=user_to_follow
        )
        messages.success(
            request, f'@{user_to_follow.username}をフォローしました')

    next_url = request.META.get('HTTP_REFERER')
    return redirect(next_url) if next_url else redirect('tweets:home')
