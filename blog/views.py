from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Post, Comment
from .forms import CommentForm


class PostList(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status='published').order_by('-created_on')
        return render(request, 'blog/blog_list.html', {'posts': posts})


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True)
        comment_form = CommentForm()
        return render(request, 'blog/blog_detail.html', {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        })

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('blog_detail', slug=slug)
        comments = post.comments.filter(approved=True)
        return render(request, 'blog/blog_detail.html', {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        })
