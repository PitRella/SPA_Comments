from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
from .forms import CommentForm
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

def comment_list(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm()

    # Получаем все корневые комментарии
    comments = Comment.objects.filter(parent__isnull=True).order_by('-created_at')
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
            # Отладочная информация о форме
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
                'text': form.cleaned_data['text']
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
