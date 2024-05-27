from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import FAQ
from .forms import CommentForm

class FAQList(View):
    def get(self, request, *args, **kwargs):
        faqs = FAQ.objects.filter(status='published').order_by('-created_on')
        return render(request, 'faq/faq_list.html', {'faqs': faqs})

class FAQDetail(View):
    def get(self, request, slug, *args, **kwargs):
        faq = get_object_or_404(FAQ, slug=slug)
        comments = faq.comments.filter(approved=True)
        new_comment = None
        comment_form = CommentForm()
        return render(request, 'faq/faq_detail.html', {
            'faq': faq,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        })
