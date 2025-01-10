from django import forms
from tweets.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-black text-white border-0',
                'rows': '1',
                'placeholder': 'コメントを投稿',
                'maxlength': '140',
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('コメントを入力してください。')
        if len(content) > 140:
            raise forms.ValidationError('コメントは140文字以内で入力してください。')
        return content
