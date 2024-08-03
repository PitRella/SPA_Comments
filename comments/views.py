from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .models import Comment
from .forms import CommentForm

def comment_list(request):
    # Обработка формы комментариев
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm()

    # Обработка сортировки
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    if order == 'asc':
        sort_by = f'-{sort_by}'

    # Получение всех корневых комментариев с учетом сортировки
    comments = Comment.objects.filter(parent__isnull=True).order_by(sort_by)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Отправка данных в формате JSON для AJAX-запроса
        comments_data = list(comments.values('username', 'email', 'created_at', 'id'))
        return JsonResponse({'comments': comments_data})

    # Отображение страницы с комментариями
    return render(request, 'comments/comment_list.html', {'form': form, 'comments': comments})

def add_reply(request, parent_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent = get_object_or_404(Comment, id=parent_id)
            reply.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    else:
        return HttpResponseBadRequest('Invalid request method')

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
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
                'text': form.cleaned_data['text'],
            }
            return JsonResponse({'preview': data['text']})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
