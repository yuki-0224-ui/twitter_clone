from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tweets.models import Tweet, Like


@login_required
def like_tweet(request, pk):
    if request.method == 'POST':
        tweet = get_object_or_404(Tweet, pk=pk)
        like = Like.objects.filter(user=request.user, tweet=tweet)

        if like.exists():
            like.delete()
        else:
            Like.objects.create(user=request.user, tweet=tweet)

        next_url = request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect('tweets:home')
