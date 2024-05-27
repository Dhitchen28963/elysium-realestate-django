from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post

class PostList(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.order_by('-id')
        return render(request, 'testimonials/testimonials_list.html', {'posts': posts})

class PostDetail(View):
    def get(self, request, id, *args, **kwargs):
        post = get_object_or_404(Post, id=id)
        return render(request, 'testimonials/testimonials_detail.html', {'post': post})
