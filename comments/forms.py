import bleach
import html5lib
from captcha.fields import CaptchaField
from django import forms
from django.core.files.base import ContentFile

from .models import Comment
from PIL import Image  # Импорт класса Image
from io import BytesIO

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

        # Clean text fields
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

        # Validate and resize image
        image = cleaned_data.get('image')
        if image:
            try:
                img = Image.open(image)
                if img.size[0] > 320 or img.size[1] > 240:
                    img.thumbnail((320, 240), Image.Resampling.LANCZOS)
                    temp_io = BytesIO()
                    img.save(temp_io, format=img.format)
                    temp_io.seek(0)
                    image_name = f"resized_{image.name}"
                    cleaned_data['image'] = ContentFile(temp_io.read(), name=image_name)
            except IOError:
                self.add_error('image', 'Invalid image file.')

        # Validate file size and format
        file = cleaned_data.get('file')
        if file:
            if file.size > 5 * 1024 * 1024:  # Limit file size to 5MB
                self.add_error('file', 'File size exceeds the 5MB limit.')
            if not file.name.endswith('.txt'):
                self.add_error('file', 'Only TXT files are allowed.')
            # Check if file content size exceeds 100 KB
            file_content = file.read()
            if len(file_content) > 100 * 1024:
                self.add_error('file', 'File size exceeds the 100KB limit.')
            file.seek(0)  # Reset file pointer after reading

        return cleaned_data