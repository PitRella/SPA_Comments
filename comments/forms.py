import bleach  # Library for sanitizing HTML inputs
import html5lib  # HTML parser for validation
from captcha.fields import CaptchaField  # CAPTCHA field for form protection
from django import forms  # Django form framework
from django.core.files.base import ContentFile  # Handles file content

from .models import Comment  # Import the Comment model
from PIL import Image  # Python Imaging Library for image processing
from io import BytesIO  # Handles byte streams

class CommentForm(forms.ModelForm):
    # Define a CAPTCHA field to protect the form from automated submissions
    captcha = CaptchaField(required=False)

    class Meta:
        model = Comment  # Specify the model to use for this form
        fields = ['username', 'email', 'homepage', 'text', 'captcha', 'parent', 'image', 'file']
        # Define widgets for the form fields
        widgets = {
            'parent': forms.HiddenInput()  # Hide the parent field as it is not editable
        }

    def clean(self):
        # Perform custom validation on the form data
        cleaned_data = super().clean()  # Call the parent class's clean method to get cleaned data

        # Define allowed HTML tags and attributes for sanitation
        ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
        ALLOWED_ATTRIBUTES = {
            'a': ['href', 'title'],
            'i': [],
            'code': [],
            'strong': [],
        }

        # Sanitize each field that may contain HTML content
        for field in ['username', 'email', 'homepage', 'text']:
            value = cleaned_data.get(field)
            if value:
                # Clean the value to allow only specified HTML tags and attributes
                cleaned_value = bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

                # Parse the cleaned HTML fragment to ensure it is properly closed
                parser = html5lib.HTMLParser(strict=True)
                try:
                    parser.parseFragment(cleaned_value)
                except html5lib.html5parser.ParseError:
                    self.add_error(field, "Message contains improperly closed HTML tags.")

                # Check if the cleaned value is different from the original value
                if cleaned_value != value:
                    self.add_error(field, "Message contains disallowed HTML tags or attributes.")

                cleaned_data[field] = cleaned_value  # Update cleaned_data with the sanitized value

        # Handle image file validation and resizing
        image = cleaned_data.get('image')
        if image:
            try:
                img = Image.open(image)  # Open the image file
                # Resize the image if its dimensions exceed 320x240 pixels
                if img.size[0] > 320 or img.size[1] > 240:
                    img.thumbnail((320, 240), Image.Resampling.LANCZOS)
                    temp_io = BytesIO()  # Create an in-memory byte stream
                    img.save(temp_io, format=img.format)  # Save the resized image to the byte stream
                    temp_io.seek(0)  # Move to the start of the byte stream
                    image_name = f"resized_{image.name}"  # Create a new name for the resized image
                    cleaned_data['image'] = ContentFile(temp_io.read(), name=image_name)  # Update cleaned_data with resized image
            except IOError:
                self.add_error('image', 'Invalid image file.')  # Add error if image cannot be processed

        # Handle file validation
        file = cleaned_data.get('file')
        if file:
            if file.size > 5 * 1024 * 1024:  # Check if file size exceeds 5MB
                self.add_error('file', 'File size exceeds the 5MB limit.')
            if not file.name.endswith('.txt'):  # Check if file is not a TXT file
                self.add_error('file', 'Only TXT files are allowed.')
            file_content = file.read()
            if len(file_content) > 100 * 1024:  # Check if file content size exceeds 100KB
                self.add_error('file', 'File size exceeds the 100KB limit.')
            file.seek(0)  # Reset file pointer to the beginning

        return cleaned_data  # Return the cleaned data
