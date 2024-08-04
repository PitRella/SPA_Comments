from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
import bleach

def sanitize_html(html):
    allowed_tags = ['b', 'i', 'u', 'a', 'p', 'br', 'ul', 'ol', 'li', 'blockquote', 'code']
    allowed_attributes = {
        'a': ['href', 'title'],
    }
    cleaned_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    return cleaned_html

def comment_list(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.text = sanitize_html(comment.text)
            comment.save()
            return redirect('comment_list')
    else:
        form = CommentForm()

    # Handle sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')

    # Default to LIFO (Last In, First Out) by sorting in descending order
    if sort_by not in ['username', 'email', 'created_at']:
        sort_by = 'created_at'
    if order not in ['asc', 'desc']:
        order = 'desc'

    # Reverse sorting order if 'desc' to ensure LIFO
    sort_by = f'-{sort_by}' if order == 'desc' else sort_by

    # Get all root comments
    comments = Comment.objects.filter(parent__isnull=True).order_by(sort_by)

    # Paginator setup
    paginator = Paginator(comments, 10)  # Show 10 comments per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'comments/comment_list.html', {'form': form, 'comments': page_obj})

def add_reply(request, parent_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.text = sanitize_html(reply.text)
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
            comment = form.save(commit=False)
            comment.text = sanitize_html(comment.text)
            comment.save()
            return redirect('comment_list')
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    return redirect('comment_list')

@csrf_exempt
def preview_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = sanitize_html(form.cleaned_data['text'])
            data = {
                'success': True,
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'text': text,
            }
            return JsonResponse({'preview': data['text']})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
