import bleach
import html5lib
from captcha.fields import CaptchaField
from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    captcha = CaptchaField(required=False)

    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'text', 'captcha', 'parent']
        widgets = {
            'parent': forms.HiddenInput()
        }

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

                parser = html5lib.HTMLParser(strict=True)
                try:
                    parser.parseFragment(cleaned_value)
                except html5lib.html5parser.ParseError:
                    self.add_error(field, "Message contains improperly closed HTML tags.")

                if cleaned_value != value:
                    self.add_error(field, "Message contains disallowed HTML tags or attributes.")

                cleaned_data[field] = cleaned_value

        return cleaned_data
