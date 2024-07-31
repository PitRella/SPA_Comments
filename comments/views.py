from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from django.http import HttpResponse

def comment_list(request):
    comments = Comment.objects.all()
    form = CommentForm()
    return render(request, 'comments/comment_list.html', {'comments': comments, 'form': form})

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    return redirect('comment_list')
