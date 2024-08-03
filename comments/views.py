from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Comment
from .forms import CommentForm
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

def comment_list(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm()

    comments_list = Comment.objects.all().order_by('-created_at')  # Используйте правильное поле для сортировки
    paginator = Paginator(comments_list, 10)  # Показывать по 10 комментариев на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'comments/comment_list.html', {'form': form, 'page_obj': page_obj})


def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    return redirect('comment_list')

def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent = parent_comment
            reply.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")

    return redirect('comment_list')

@csrf_exempt
def preview_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = {
                'success': True,
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'text': form.cleaned_data['text']
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
