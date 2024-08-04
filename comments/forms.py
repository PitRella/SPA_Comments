import bleach
import html5lib
from captcha.fields import CaptchaField
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    captcha = CaptchaField(required=False)

    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'text', 'captcha', 'parent', 'image', 'file']
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

        # Validate image size
        image = cleaned_data.get('image')
        if image:
            from PIL import Image
            from io import BytesIO

            img = Image.open(image)
            if img.size[0] > 320 or img.size[1] > 240:
                img.thumbnail((320, 240), Image.ANTIALIAS)
                temp_io = BytesIO()
                img.save(temp_io, format=img.format)
                temp_io.seek(0)
                image.file = temp_io

            if image.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                self.add_error('image', 'Unsupported file format. Only JPG, PNG, and GIF are allowed.')

        # Validate file size and format
        file = cleaned_data.get('file')
        if file:
            if file.size > 5 * 1024 * 1024:  # Limit file size to 5MB
                self.add_error('file', 'File size exceeds the 5MB limit.')

        return cleaned_data
