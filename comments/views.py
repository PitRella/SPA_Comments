from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
import bleach

# Function to sanitize HTML content, allowing only certain tags and attributes
def sanitize_html(html):
    allowed_tags = ['b', 'i', 'u', 'a', 'p', 'br', 'ul', 'ol', 'li', 'blockquote', 'code']
    allowed_attributes = {
        'a': ['href', 'title'],
    }
    cleaned_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    return cleaned_html

# View to display a list of comments and handle comment submission
def comment_list(request):
    if request.method == 'POST':
        # Handle form submission
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.text = sanitize_html(comment.text)  # Sanitize comment text
            comment.save()  # Save the new comment
            return redirect('comment_list')  # Redirect to the comment list page
    else:
        form = CommentForm()  # Create an empty form for GET requests

    # Handling sorting and pagination
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')

    # Validate sorting and ordering parameters
    if sort_by not in ['username', 'email', 'created_at']:
        sort_by = 'created_at'
    if order not in ['asc', 'desc']:
        order = 'desc'

    sort_by = f'-{sort_by}' if order == 'desc' else sort_by

    # Get comments that do not have parents (top-level comments)
    comments = Comment.objects.filter(parent__isnull=True).order_by(sort_by)

    # Paginate comments, showing 25 per page
    paginator = Paginator(comments, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the comment list page with the form and paginated comments
    return render(request, 'comments/comment_list.html', {'form': form, 'comments': page_obj})

# View to handle adding a reply to an existing comment
def add_reply(request, parent_id):
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.text = sanitize_html(reply.text)  # Sanitize reply text
            reply.parent = get_object_or_404(Comment, id=parent_id)  # Set the parent comment
            reply.save()  # Save the reply
            return redirect('comment_list')  # Redirect to the comment list page
        else:
            return HttpResponse(f"Form errors: {form.errors}")  # Return form errors as HTTP response
    else:
        return HttpResponseBadRequest('Invalid request method')  # Return error for invalid request method

# View to handle adding a new comment
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.text = sanitize_html(comment.text)  # Sanitize comment text
            comment.save()  # Save the new comment
            return redirect('comment_list')  # Redirect to the comment list page
        else:
            return HttpResponse(f"Form errors: {form.errors}")  # Return form errors as HTTP response
    return redirect('comment_list')  # Redirect to the comment list page for non-POST requests

# View to handle previewing a comment via AJAX
@csrf_exempt
def preview_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = sanitize_html(form.cleaned_data['text'])  # Sanitize preview text
            data = {
                'success': True,
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'text': text,
            }
            return JsonResponse({'preview': data['text']})  # Return the sanitized text as JSON
        else:
            return JsonResponse({'error': form.errors}, status=400)  # Return form errors as JSON with 400 status
    return JsonResponse({'error': 'Invalid request'}, status=400)  # Return error for invalid request method
