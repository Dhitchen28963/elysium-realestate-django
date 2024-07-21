from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostList(ListView):
    model = Post
    template_name = 'property_guides/property_guides_list.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'property_guides/property_guides_detail.html'


def property_guides_list(request):
    posts = Post.objects.all()
    landlord_guides = posts.filter(category__name='Landlord')
    renter_guides = posts.filter(category__name='Renter')
    student_guides = posts.filter(category__name='Student')
    neighbour_disputes = posts.filter(category__name='Neighbour Disputes')

    context = {
        'landlord_guides': landlord_guides,
        'renter_guides': renter_guides,
        'student_guides': student_guides,
        'neighbour_disputes': neighbour_disputes,
    }

    return render(
        request,
        'property_guides/property_guides_list.html',
        context
    )


def property_guides_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(
        request,
        'property_guides/property_guides_detail.html',
        {'post': post}
    )


def property_guides_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts,
    }

    return render(
        request,
        'property_guides/property_guides_category.html',
        context
    )
