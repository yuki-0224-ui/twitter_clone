from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model


class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '電話番号を入力',
                'type': 'tel',
            }
        ),
        label='電話番号（任意）'
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ),
        label='生年月日（任意）'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ユーザー名を入力'
        })
        self.fields['username'].label = 'ユーザー名'

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'メールアドレスを入力'
        })
        self.fields['email'].label = 'メールアドレス'

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワードを入力'
        })
        self.fields['password1'].label = 'パスワード'

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワードを再入力'
        })
        self.fields['password2'].label = 'パスワード（確認）'

    def clean_email(self):
        email = self.cleaned_data['email']

        if email:
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username:
            User = get_user_model()
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError("このユーザー名は既に使用されています。")

        return username

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.save()
        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ユーザー名またはメールアドレスを入力'
        })
        self.fields['login'].label = 'ユーザー名またはメールアドレス'

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワードを入力'
        })
        self.fields['password'].label = 'パスワード'
