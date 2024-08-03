import bleach
from captcha.fields import CaptchaField
from django import forms
from .models import Comment, Reply
from django.core.exceptions import ValidationError

class CaptchaCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'text', 'captcha']

    def clean_text(self):
        value = self.cleaned_data.get('text')
        ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
        ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title'],
            'i': [],
            'code': [],
            'strong': [],
        }

        cleaned_value = bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
        if cleaned_value != value:
            raise ValidationError("Message contains disallowed HTML tags or attributes.")
        return cleaned_value

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['username', 'email', 'homepage', 'text']
