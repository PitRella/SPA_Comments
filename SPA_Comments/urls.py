from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from comments import views

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Include URLs from the 'comments' app
    path('', include('comments.urls')),

    # Additional URL patterns for handling comments and replies
    path('add/', views.add_comment, name='add_comment'),
    path('reply/<int:parent_id>/', views.add_reply, name='add_reply'),
    path('preview_comment/', views.preview_comment, name='preview_comment'),
]

# Include CAPTCHA URL patterns
urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)