from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tweet, Follow, Like, Retweet, Comment


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'username', 'password')}),
        ('個人情報', {'fields': ('email', 'phone_number', 'display_name', 'bio',
         'location', 'website', 'date_of_birth', 'profile_image', 'header_image')}),
        ('権限', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('重要な日付', {'fields': ('last_login',
         'date_joined', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_preview', 'created_at')
    search_fields = ('content', 'user__username')
    fields = ('id', 'user', 'content')
    readonly_fields = ('id',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'ツイート内容'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'followee', 'created_at')
    search_fields = ('follower__username', 'followee__username')
    fields = ('id', 'follower', 'followee')
    readonly_fields = ('id',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tweet', 'created_at')
    search_fields = ('user__username', 'tweet__content')
    fields = ('id', 'user', 'tweet')
    readonly_fields = ('id',)


@admin.register(Retweet)
class RetweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tweet', 'created_at')
    search_fields = ('user__username', 'tweet__content')
    fields = ('id', 'user', 'tweet')
    readonly_fields = ('id',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tweet', 'content_preview', 'created_at')
    search_fields = ('content', 'user__username', 'tweet__content')
    fields = ('id', 'user', 'tweet', 'parent_comment', 'content')
    readonly_fields = ('id',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'コメント内容'


admin.site.register(CustomUser, CustomUserAdmin)
