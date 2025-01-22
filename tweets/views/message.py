from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from tweets.models import MessageRoom
from tweets.forms import MessageForm
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageRoomListView(LoginRequiredMixin, ListView):
    model = MessageRoom
    template_name = 'room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return MessageRoom.get_rooms_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = MessageForm()

        room_id = self.request.GET.get('room')
        if room_id:
            selected_room = MessageRoom.get_room_with_messages(
                room_id, self.request.user)
            if selected_room:
                context.update({
                    'selected_room': selected_room,
                    'room_messages': selected_room.all_messages,
                    'other_user': selected_room.other_user(self.request.user)
                })

        return context

    def post(self, request, *args, **kwargs):
        room_id = request.POST.get('room_id')
        if not room_id:
            messages.error(request, 'メッセージの送信に失敗しました')
            return redirect('tweets:messages')

        form = MessageForm(request.POST)
        if not form.is_valid():
            return self.get(request, *args, **kwargs)

        message = MessageRoom.create_message_from_form(
            room_id, request.user, form.cleaned_data['content'])

        if message:
            return redirect(f'{request.path}?room={room_id}')

        messages.error(request, 'メッセージルームが見つかりません')
        return redirect('tweets:messages')


def create_message_room(request, username):
    if request.method != 'POST':
        return redirect('tweets:messages')

    room, other_user, error = MessageRoom.create_room_for_users(
        request.user, username)

    if error == 'ユーザーが見つかりません':
        messages.error(request, error)
        return redirect('tweets:messages')

    if error == 'existing':
        messages.info(request, f'{other_user.username}とのメッセージルームに移動します')
    else:
        messages.success(request, f'{other_user.username}とのメッセージルームを作成しました')

    return redirect(f'/messages/?room={room.id}')


message_room_list = MessageRoomListView.as_view()
