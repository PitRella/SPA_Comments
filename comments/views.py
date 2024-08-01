from django.shortcuts import render, redirect
from .models import Comment
from .forms import CaptchaCommentForm
from django.http import HttpResponse

def comment_list(request):
    comments = Comment.objects.all()
    form = CaptchaCommentForm()
    return render(request, 'comments/comment_list.html', {'comments': comments, 'form': form})

def add_comment(request):
    if request.method == 'POST':
        form = CaptchaCommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    return redirect('comment_list')
