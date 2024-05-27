from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post
from .forms import CommentForm

class PostList(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status='published').order_by('-created_on')
        return render(request, 'blog/blog_list.html', {'posts': posts})

class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True)
        new_comment = None
        comment_form = CommentForm()
        return render(request, 'blog/blog_detail.html', {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        })
