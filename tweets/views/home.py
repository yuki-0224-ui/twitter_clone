from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib import messages
from tweets.models import Tweet
from tweets.forms import TweetForm


class HomeView(ListView):
    model = Tweet
    template_name = 'home.html'
    context_object_name = 'tweets'
    paginate_by = 10

    TAB_RECOMMENDED = 'recommended'
    TAB_FOLLOWING = 'following'

    def get_tab(self):
        return self.request.GET.get('tab', self.TAB_RECOMMENDED)

    def get_queryset(self):
        tab = self.get_tab()
        if tab == self.TAB_FOLLOWING:
            return Tweet.get_following_timeline_for_user(self.request.user)
        return Tweet.get_timeline_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TweetForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, 'ツイートを投稿しました。')
            return redirect('tweets:home')

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


home = HomeView.as_view()
