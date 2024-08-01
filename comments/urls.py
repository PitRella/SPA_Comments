from .views import comment_list, add_comment
from django.urls import path, include

urlpatterns = [
    path('', comment_list, name='comment_list'),
    path('add/', add_comment, name='add_comment'),
]
