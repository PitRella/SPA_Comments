from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Reply
from .forms import CaptchaCommentForm, ReplyForm
from django.http import HttpResponse
from django.core.paginator import Paginator


def comment_list(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')  # Сортировка по умолчанию – убывание

    valid_sort_fields = ['username', 'email', 'created_at']

    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'

    if order == 'asc':
        comments = Comment.objects.all().order_by(sort_by)
    else:
        comments = Comment.objects.all().order_by(f'-{sort_by}')

    paginator = Paginator(comments, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = CaptchaCommentForm()
    reply_form = ReplyForm()  # Добавлено для обработки ответа

    return render(request, 'comments/comment_list.html', {
        'page_obj': page_obj,
        'form': form,
        'reply_form': reply_form,
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


def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")

    return redirect('comment_list')