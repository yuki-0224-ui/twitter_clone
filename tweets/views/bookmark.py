from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tweets.models import Tweet, Bookmark


@login_required
def bookmark_tweet(request, pk):
    if request.method == 'POST':
        tweet = get_object_or_404(Tweet, pk=pk)
        bookmark = Bookmark.objects.filter(user=request.user, tweet=tweet)
        if bookmark.exists():
            bookmark.delete()
        else:
            Bookmark.objects.create(user=request.user, tweet=tweet)
        next_url = request.META.get('HTTP_REFERER')
        if next_url:
            return redirect(next_url)
        return redirect('tweets:home')


class BookmarkListView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'bookmark_list.html'
    context_object_name = 'tweets'
    paginate_by = 10

    def get_queryset(self):
        return Tweet.with_interaction_details(self.request.user).filter(
            bookmarks__user=self.request.user
        )

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        try:
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.page(1)
        return (paginator, page_obj, page_obj.object_list, page_obj.has_other_pages())


bookmark_list = BookmarkListView.as_view()
