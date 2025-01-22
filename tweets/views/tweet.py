from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from tweets.models import Tweet, Notification
from tweets.forms import CommentForm


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = 'tweet_detail.html'
    context_object_name = 'tweet'

    def get_queryset(self):
        return Tweet.with_interaction_details(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related(
            'user').order_by('created_at')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = self.object
            comment.save()

            if request.user != self.object.user:
                Notification.create_notification(
                    recipient=self.object.user,
                    actor=request.user,
                    notification_type=Notification.COMMENT,
                    tweet=self.object
                )

            messages.success(request, 'コメントを投稿しました。')
            return redirect('tweets:tweet_detail', pk=self.object.pk)

        context = self.get_context_data(form=form)
        context['form'] = form
        return self.render_to_response(context)


tweet_detail = TweetDetailView.as_view()
