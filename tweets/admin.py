from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('個人情報', {'fields': (
            'email',
            'phone_number',
            'display_name',
            'bio',
            'location',
            'website',
            'date_of_birth',
            'profile_image_url',
            'header_image_url'
        )}),
        ('権限', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('重要な日付', {'fields': ('last_login',
         'date_joined', 'created_at', 'updated_at')}),
    )

    readonly_fields = ('created_at', 'updated_at')


admin.site.register(CustomUser, CustomUserAdmin)
