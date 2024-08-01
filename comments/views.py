from django.shortcuts import render, redirect
from .models import Comment
from .forms import CaptchaCommentForm
from django.http import HttpResponse

def comment_list(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')

    if order == 'asc':
        comments = Comment.objects.all().order_by(sort_by)
    else:
        comments = Comment.objects.all().order_by(f'-{sort_by}')

    form = CaptchaCommentForm()
    return render(request, 'comments/comment_list.html', {'comments': comments, 'form': form, 'sort_by': sort_by, 'order': order})

def add_comment(request):
    if request.method == 'POST':
        form = CaptchaCommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    return redirect('comment_list')
