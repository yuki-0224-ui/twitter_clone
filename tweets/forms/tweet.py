from django import forms
from tweets.models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'id': 'post-textarea',
                    'class': 'form-control bg-black text-white border-0',
                    'rows': '3',
                    'placeholder': 'いまどうしてる？',
                    'maxlength': '140',
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')

        if not content and not image:
            raise forms.ValidationError('テキストか画像のどちらかを投稿してください。')

        if content and len(content) > 140:
            raise forms.ValidationError('テキストは140文字以内で入力してください。')

        return cleaned_data
