from django.views.generic import DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from tweets.models import Tweet
from tweets.forms import ProfileEditForm
from django.urls import reverse_lazy
from django.contrib import messages

User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = 10

    TAB_TWEETS = 'tweets'
    TAB_LIKES = 'likes'
    TAB_RETWEETS = 'retweets'
    TAB_COMMENTS = 'comments'

    def get_tab(self):
        return self.request.GET.get('tab', self.TAB_TWEETS)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        tab = self.get_tab()

        tweets = self._get_tweets_for_tab(profile_user, tab)
        total_count = len(tweets)

        paginator = Paginator(tweets, self.paginate_by)
        page_obj = paginator.get_page(self.request.GET.get('page', 1))

        context.update({
            'tweets': page_obj,
            'total_count': total_count,
            'following_count': profile_user.following.count(),
            'followers_count': profile_user.followers.count(),
            'is_following': self.request.user.following.filter(followee=profile_user).exists()
            if self.request.user != profile_user else False
        })

        return context

    def _get_tweets_for_tab(self, user, tab):
        if tab == self.TAB_TWEETS:
            return Tweet.get_user_timeline(user)
        elif tab == self.TAB_LIKES:
            return Tweet.get_liked_by(user)
        elif tab == self.TAB_RETWEETS:
            return Tweet.get_retweeted_by(user)
        elif tab == self.TAB_COMMENTS:
            return Tweet.get_commented_by(user)
        return Tweet.get_user_timeline(user)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, 'プロフィールを更新しました')
        return reverse_lazy('tweets:profile', kwargs={'username': self.request.user.username})


profile = ProfileView.as_view()
profile_edit = ProfileEditView.as_view()
