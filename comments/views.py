from django.shortcuts import render, redirect
from .models import Comment
from .forms import CaptchaCommentForm
from django.http import HttpResponse
from django.core.paginator import Paginator

def comment_list(request):
    sort_by = request.GET.get('sort_by', 'created_at')  # По умолчанию сортируем по дате добавления
    order = request.GET.get('order', 'desc')  # По умолчанию сортируем по убыванию

    valid_sort_fields = ['username', 'email', 'created_at']

    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'

    if order == 'asc':
        comments = Comment.objects.all().order_by(sort_by)
    else:
        comments = Comment.objects.all().order_by(f'-{sort_by}')

    paginator = Paginator(comments, 25)  # 25 комментариев на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = CaptchaCommentForm()
    return render(request, 'comments/comment_list.html', {
        'page_obj': page_obj,
        'form': form,
        'sort_by': sort_by,
        'order': order
    })
def add_comment(request):
    if request.method == 'POST':
        form = CaptchaCommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    return redirect('comment_list')
