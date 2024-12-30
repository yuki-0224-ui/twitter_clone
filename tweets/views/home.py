from django.views.generic import ListView
from tweets.models import Tweet


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
        return Tweet.get_timeline_for_user()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_tab'] = self.get_tab()
        return context


home = HomeView.as_view()
