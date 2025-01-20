from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q, Prefetch

User = get_user_model()


class MessageRoom(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_rooms_as_user1'
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_rooms_as_user2'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user1', 'user2']
        ordering = ['-updated_at']

    def __str__(self):
        return f'Chat: {self.user1.username} - {self.user2.username}'

    def other_user(self, user):
        return self.user2 if user == self.user1 else self.user1

    @classmethod
    def _base_room_queryset(cls, user):
        return cls.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).select_related('user1', 'user2')

    @classmethod
    def get_or_create_room(cls, user1, user2):
        room = cls.objects.filter(
            models.Q(user1=user1, user2=user2) |
            models.Q(user1=user2, user2=user1)
        ).first()

        if not room:
            room = cls.objects.create(user1=user1, user2=user2)

        return room

    @classmethod
    def create_room_for_users(cls, user1, username):
        try:
            other_user = User.objects.get(username=username)
            room = cls.objects.filter(
                models.Q(user1=user1, user2=other_user) |
                models.Q(user1=other_user, user2=user1)
            ).first()

            if room:
                return room, other_user, 'existing'

            room = cls.objects.create(user1=user1, user2=other_user)
            return room, other_user, 'created'

        except User.DoesNotExist:
            return None, None, 'ユーザーが見つかりません'

    @classmethod
    def get_rooms_for_user(cls, user):
        rooms = cls._base_room_queryset(user).prefetch_related(
            Prefetch(
                'messages',
                queryset=Message.objects.order_by('-created_at'),
                to_attr='latest_messages'
            )
        )

        for room in rooms:
            room.other_user_cache = room.user2 if room.user1 == user else room.user1
            room.latest_message_content = room.latest_messages[
                0].content if room.latest_messages else None

        return rooms

    @classmethod
    def get_room_with_messages(cls, room_id, user):
        try:
            room = cls._base_room_queryset(user).filter(
                id=room_id
            ).prefetch_related(
                Prefetch(
                    'messages',
                    queryset=Message.objects.select_related(
                        'sender').order_by('created_at'),
                    to_attr='all_messages'
                )
            ).get()
            return room
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_message_from_form(cls, room_id, user, content):
        try:
            room = cls._base_room_queryset(user).get(id=room_id)
            message = Message.create_message(
                room=room,
                sender=user,
                content=content
            )
            return message
        except cls.DoesNotExist:
            return None


class Message(models.Model):
    room = models.ForeignKey(
        MessageRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}... ({self.created_at.strftime("%Y-%m-%d %H:%M")})'

    @classmethod
    def create_message(cls, room, sender, content):
        message = cls.objects.create(
            room=room,
            sender=sender,
            content=content
        )
        room.save(update_fields=['updated_at'])
        return message
