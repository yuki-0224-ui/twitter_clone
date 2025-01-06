from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['display_name', 'bio', 'location', 'website',
                  'date_of_birth', 'profile_image', 'header_image']

        base_attrs = {'class': 'form-control bg-black text-white'}

        widgets = {
            'display_name': forms.TextInput(
                attrs={
                    **base_attrs,
                    'placeholder': '表示名'
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    **base_attrs,
                    'placeholder': '自己紹介',
                    'rows': 3
                }
            ),
            'location': forms.TextInput(
                attrs={
                    **base_attrs,
                    'placeholder': '場所'
                }
            ),
            'website': forms.URLInput(
                attrs={
                    **base_attrs,
                    'placeholder': 'ウェブサイト'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    **base_attrs,
                    'type': 'date'
                }
            ),
            'profile_image': forms.FileInput(
                attrs={
                    **base_attrs,
                    'accept': 'image/jpeg,image/png'
                }
            ),
            'header_image': forms.FileInput(
                attrs={
                    **base_attrs,
                    'accept': 'image/jpeg,image/png'
                }
            )
        }

        labels = {
            'display_name': '表示名',
            'bio': '自己紹介',
            'location': '場所',
            'website': 'ウェブサイト',
            'date_of_birth': '生年月日',
            'profile_image': 'プロフィール画像（JPEGまたはPNG形式、5MB以下）',
            'header_image': 'ヘッダー画像（JPEGまたはPNG形式、5MB以下）'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        image_fields = ['profile_image', 'header_image']

        for field in image_fields:
            self.fields[field].validators.append(
                FileExtensionValidator(['jpg', 'jpeg', 'png'])
            )
            self.fields[field].required = False
