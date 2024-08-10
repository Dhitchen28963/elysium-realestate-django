from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category

"""
Displays a list of all posts in the property guides section.
Utilizes Django's ListView to handle the context and template.
"""


class PostList(ListView):
    model = Post
    template_name = 'property_guides/property_guides_list.html'
    context_object_name = 'posts'


"""
Displays the details of a specific post in the property guides section.
Utilizes Django's DetailView to handle the context and template.
"""


class PostDetail(DetailView):
    model = Post
    template_name = 'property_guides/property_guides_detail.html'


"""
Handles the display of a specific property guide's details based on the slug.
Uses get_object_or_404 to fetch the post or return a 404 error if not found.
"""


def property_guides_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(
        request,
        'property_guides/property_guides_detail.html',
        {'post': post}
    )


"""
Handles the display of all property guides, categorized by different
guide topics such as Landlord, Renter, Student, Complaints, etc.
Filters posts by category and passes them to the template for display.
"""


def property_guides_list(request):
    posts = Post.objects.all()
    landlord_guides = posts.filter(category__name='Landlord')
    renter_guides = posts.filter(category__name='Renter')
    student_guides = posts.filter(category__name='Student')
    complaints_guides = posts.filter(category__name='Complaints')
    neighbour_disputes = posts.filter(category__name='Neighbour Disputes')
    fire_safety_guides = posts.filter(category__name='Fire Safety')
    repairs_guides = posts.filter(category__name='Repairs')
    eviction_guides = posts.filter(category__name='Eviction')
    mortgage_guides = posts.filter(category__name='Mortgage')
    buying_selling_guides = posts.filter(category__name='Buyers/Selling')

    context = {
        'landlord_guides': landlord_guides,
        'renter_guides': renter_guides,
        'student_guides': student_guides,
        'complaints_guides': complaints_guides,
        'neighbour_disputes': neighbour_disputes,
        'fire_safety_guides': fire_safety_guides,
        'repairs_guides': repairs_guides,
        'eviction_guides': eviction_guides,
        'mortgage_guides': mortgage_guides,
        'buying_selling_guides': buying_selling_guides,
    }

    return render(
        request,
        'property_guides/property_guides_list.html',
        context
    )


"""
Handles the display of property guides filtered by a specific category.
Fetches the category and corresponding posts, then passes them to the template.
"""


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
