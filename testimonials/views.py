from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Testimonial
from .forms import TestimonialForm

@login_required
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'testimonials/testimonials_list.html', {'testimonials': testimonials})

@login_required
def testimonials_detail(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    return render(request, 'testimonials/testimonials_detail.html', {'testimonial': testimonial})

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.author = request.user
            testimonial.save()
            return redirect('testimonials_list')
    else:
        form = TestimonialForm()
    return render(request, 'testimonials/add_testimonial.html', {'form': form})

@login_required
def edit_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save()
            return redirect('testimonials_detail', pk=testimonial.pk)
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'testimonials/edit_testimonial.html', {'form': form})

@login_required
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        return redirect('testimonials_list')
    return render(request, 'testimonials/delete_testimonial.html', {'testimonial': testimonial})
