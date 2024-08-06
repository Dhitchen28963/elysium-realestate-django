from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db import models
from .models import Blog, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, JsonResponse
import json

class BlogList(View):
    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.filter(status='published').order_by('-created_on')
        return render(request, 'blog/blog_list.html', {'blogs': blogs})

class BlogDetail(View):
    def get(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        comments = blog.comments.filter(models.Q(approved=True) | models.Q(author=request.user))
        comment_form = CommentForm()
        return render(request, 'blog/blog_detail.html', {
            'blog': blog,
            'comments': comments,
            'comment_form': comment_form
        })

    @method_decorator(login_required)
    def post(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = blog
            new_comment.author = request.user
            new_comment.approved = False  # Comment needs approval
            new_comment.pending_approval = True
            new_comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'comment': new_comment.body, 'pending': True})
            return redirect('blog_detail', slug=slug)
        comments = blog.comments.filter(models.Q(approved=True) | models.Q(author=request.user))
        return render(request, 'blog/blog_detail.html', {
            'blog': blog,
            'comments': comments,
            'comment_form': comment_form
        })

@method_decorator(login_required, name='dispatch')
class BlogCommentEdit(View):
    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return HttpResponseForbidden()
        
        try:
            data = json.loads(request.body)
            form = CommentForm(data, instance=comment)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'})

        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = False  # Mark as pending approval
            comment.pending_approval = True
            comment.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Form is not valid.'})

@login_required
def delete_blog_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return HttpResponseForbidden()
    comment.delete()
    return JsonResponse({'success': True})
