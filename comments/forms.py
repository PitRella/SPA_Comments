from django import forms
from .models import Comment
from captcha.fields import CaptchaField

class CaptchaCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'captcha', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }