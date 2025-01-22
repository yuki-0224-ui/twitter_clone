from django import forms
from tweets.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control bg-black text-white border-secondary',
                    'rows': '1',
                    'placeholder': 'メッセージを入力...',
                    'style': 'resize: none;'
                }
            )
        }
