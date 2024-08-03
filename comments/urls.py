from .views import comment_list, add_comment, add_reply, preview_comment
from django.urls import path, include

urlpatterns = [
    path('', comment_list, name='comment_list'),
    path('add/', add_comment, name='add_comment'),
    path('add_reply/<int:comment_id>/', add_reply, name='add_reply'),
    path('preview_comment/', preview_comment, name='preview_comment'),

]
