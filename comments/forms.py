import bleach
import html5lib
from captcha.fields import CaptchaField
from django import forms
from .models import Comment, Reply
from django.core.exceptions import ValidationError

class CaptchaCommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'text', 'captcha']

    def clean(self):
        cleaned_data = super().clean()
        ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
        ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title'],
            'i': [],
            'code': [],
            'strong': [],
        }

        for field in ['username', 'email', 'homepage', 'text']:
            value = cleaned_data.get(field)
            if value:
                cleaned_value = bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

                # Validate with html5lib to check for closed tags
                parser = html5lib.HTMLParser(strict=True)
                try:
                    parser.parseFragment(cleaned_value)
                except html5lib.html5parser.ParseError:
                    self.add_error(field, "Message contains improperly closed HTML tags.")

                if cleaned_value != value:
                    self.add_error(field, "Message contains disallowed HTML tags or attributes.")

                cleaned_data[field] = cleaned_value

        return cleaned_data

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['username', 'email', 'homepage', 'text']
