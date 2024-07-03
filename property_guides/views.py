from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    template_name = 'property_guides/property_guides_list.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'property_guides/property_guides_detail.html'

def property_guides_list(request):
    posts = Post.objects.all()
    landlord_guides = posts.filter(category='Landlord')
    renter_guides = posts.filter(category='Renter')
    student_guides = posts.filter(category='Student')
    neighbour_disputes = posts.filter(category='Neighbour Disputes')

    context = {
        'landlord_guides': landlord_guides,
        'renter_guides': renter_guides,
        'student_guides': student_guides,
        'neighbour_disputes': neighbour_disputes,
    }

    return render(request, 'property_guides/property_guides_list.html', context)

def property_guides_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'property_guides/property_guides_detail.html', {'post': post})

def view_land(request):
    return render(request, 'property_guides/view_land.html')

def repairs(request):
    return render(request, 'property_guides/repairs.html')

def fire_safety(request):
    return render(request, 'property_guides/fire_safety.html')

def complaints(request):
    return render(request, 'property_guides/complaints.html')

def eviction(request):
    return render(request, 'property_guides/eviction.html')