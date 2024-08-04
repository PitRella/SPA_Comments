from django.db import models

class Comment(models.Model):
    # The username of the person making the comment
    username = models.CharField(max_length=100)

    # The email address of the person making the comment
    email = models.EmailField()

    # An optional field for the user's homepage URL
    homepage = models.URLField(blank=True, null=True)

    # CAPTCHA value for spam protection
    captcha = models.CharField(max_length=48)

    # The main text content of the comment
    text = models.TextField()

    # Timestamp indicating when the comment was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional foreign key to support threaded comments (replies)
    parent = models.ForeignKey(
        'self',  # Self-referential foreign key for replies
        related_name='replies',  # Allows reverse access to all replies to a comment
        on_delete=models.CASCADE,  # Cascade delete - if a parent comment is deleted, all its replies are also deleted
        blank=True,  # This field is optional
        null=True,  # This field can be null
        default=None,  # Default value for the field
        verbose_name="Parent comment"  # Human-readable name for the field
    )

    # Optional field for uploading images with comments
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)

    # Optional field for uploading files with comments
    file = models.FileField(upload_to='comment_files/', blank=True, null=True)

    def __str__(self):
        # Returns a string representation of the comment including the username and first 20 characters of the text
        return f'{self.username} - {self.text[:20]}'

    class Meta:
        # Orders comments by creation date in descending order (newest first)
        ordering = ['-created_at']
        # Verbose names for the model
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
