from .views import comment_list, add_comment, add_reply, preview_comment
from django.urls import path

# URL patterns for the application
urlpatterns = [
    # Route for displaying the list of comments
    path('', comment_list, name='comment_list'),

    # Route for adding a new comment
    path('add/', add_comment, name='add_comment'),

    # Route for adding a reply to an existing comment
    # <int:parent_id> captures an integer from the URL and passes it as `parent_id` to the view
    path('reply/<int:parent_id>/', add_reply, name='add_reply'),

    # Route for previewing a comment (e.g., before submission)
    path('preview_comment/', preview_comment, name='preview_comment'),
]
