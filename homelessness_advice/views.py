from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post


class PostList(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(status='published').order_by('-created_on')
        return render(
            request,
            'homelessness_advice/homelessness_advice_list.html',
            {'posts': posts}
        )


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        return render(
            request,
            'homelessness_advice/homelessness_advice_detail.html',
            {'post': post}
        )
