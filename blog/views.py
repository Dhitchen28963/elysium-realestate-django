from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Blog, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden

class BlogList(View):
    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.filter(status='published').order_by('-created_on')
        return render(request, 'blog/blog_list.html', {'blogs': blogs})

class BlogDetail(View):
    def get(self, request, slug, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        comments = blog.comments.filter(approved=True)
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
            new_comment.save()
            return redirect('blog_detail', slug=slug)
        comments = blog.comments.filter(approved=True)
        return render(request, 'blog/blog_detail.html', {
            'blog': blog,
            'comments': comments,
            'comment_form': comment_form
        })

@method_decorator(login_required, name='dispatch')
class BlogCommentEdit(View):
    def get(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return HttpResponseForbidden()
        form = CommentForm(instance=comment)
        return render(request, 'blog/edit_comment.html', {'form': form})

    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return HttpResponseForbidden()
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=comment.post.slug)
        return render(request, 'blog/edit_comment.html', {'form': form})

@login_required
def delete_blog_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return HttpResponseForbidden()
    blog = comment.post.slug
    comment.delete()
    return redirect('blog_detail', slug=blog)
