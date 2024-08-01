from captcha.fields import CaptchaField
from django import forms
from .models import Comment, Reply
from django.core.exceptions import ValidationError

class CaptchaCommentForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'text', 'captcha']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['username', 'email', 'homepage', 'text']
