from django.db import models
from captcha.fields import CaptchaField

class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)
    captcha = models.CharField(max_length=48)  # Сохраняем капчу как строку
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        related_name='replies',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        verbose_name="Parent comment"
    )

    def __str__(self):
        return f'{self.username} - {self.text[:20]}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
