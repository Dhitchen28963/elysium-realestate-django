from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import FAQ, Comment
from .forms import CommentForm
import json

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

    @method_decorator(login_required)
    def post(self, request, slug, *args, **kwargs):
        faq = get_object_or_404(FAQ, slug=slug)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = faq
            new_comment.author = request.user
            new_comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'comment': new_comment.body})
            return redirect('faq_detail', slug=slug)
        comments = faq.comments.filter(approved=True)
        return render(request, 'faq/faq_detail.html', {
            'faq': faq,
            'comments': comments,
            'comment_form': comment_form
        })

@method_decorator(login_required, name='dispatch')
class FAQCommentEdit(View):
    def post(self, request, comment_id, *args, **kwargs):
        print(f"Received request to edit comment with id {comment_id}")
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return HttpResponseForbidden()
        
        try:
            data = json.loads(request.body)
            form = CommentForm(data, instance=comment)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'})

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Form is not valid.'})

@login_required
def delete_faq_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return HttpResponseForbidden()
    comment.delete()
    return JsonResponse({'success': True})
