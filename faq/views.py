from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import FAQ, Comment
from .forms import CommentForm


class FAQList(View):
    def get(self, request, *args, **kwargs):
        faqs = FAQ.objects.filter(status='published').order_by('-created_on')
        return render(request, 'faq/faq_list.html', {'faqs': faqs})


class FAQDetail(View):
    def get(self, request, slug, *args, **kwargs):
        faq = get_object_or_404(FAQ, slug=slug)
        comments = faq.comments.filter(approved=True)
        comment_form = CommentForm()
        return render(request, 'faq/faq_detail.html', {
            'faq': faq,
            'comments': comments,
            'comment_form': comment_form
        })

    def post(self, request, slug, *args, **kwargs):
        faq = get_object_or_404(FAQ, slug=slug)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = faq
            new_comment.author = request.user
            new_comment.save()
            return redirect('faq_detail', slug=slug)
        comments = faq.comments.filter(approved=True)
        return render(request, 'faq/faq_detail.html', {
            'faq': faq,
            'comments': comments,
            'comment_form': comment_form
        })
