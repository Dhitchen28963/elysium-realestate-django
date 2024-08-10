from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.db import models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import FAQ, Comment
from .forms import CommentForm
import json

"""
Handles the display of the FAQ list page, showing all published FAQs
in descending order of creation date.
"""


class FAQList(View):
    def get(self, request, *args, **kwargs):
        faqs = FAQ.objects.filter(status='published').order_by('-created_on')
        return render(request, 'faq/faq_list.html', {'faqs': faqs})


"""
Handles the display and submission of comments on a FAQ detail page.
Authenticated users can see their own pending comments alongside
approved ones.
"""


class FAQDetail(View):
    def get(self, request, slug, *args, **kwargs):
        faq = get_object_or_404(FAQ, slug=slug)
        if request.user.is_authenticated:
            comments = faq.comments.filter(
                models.Q(approved=True) | models.Q(author=request.user)
            )
        else:
            comments = faq.comments.filter(approved=True)
        comment_form = CommentForm()
        return render(
            request,
            'faq/faq_detail.html',
            {
                'faq': faq,
                'comments': comments,
                'comment_form': comment_form,
                'is_authenticated': request.user.is_authenticated,
            },
        )

    @method_decorator(login_required)
    def post(self, request, slug, *args, **kwargs):
        faq = get_object_or_404(FAQ, slug=slug)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = faq
            new_comment.author = request.user
            new_comment.approved = False  # Comment needs approval
            new_comment.pending_approval = True
            new_comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    {
                        'success': True,
                        'comment': new_comment.body,
                        'pending': True,
                    }
                )
            return redirect('faq_detail', slug=slug)
        if request.user.is_authenticated:
            comments = faq.comments.filter(
                models.Q(approved=True) | models.Q(author=request.user)
            )
        else:
            comments = faq.comments.filter(approved=True)
        return render(
            request,
            'faq/faq_detail.html',
            {
                'faq': faq,
                'comments': comments,
                'comment_form': comment_form,
                'is_authenticated': request.user.is_authenticated,
            },
        )


"""
Handles the editing of comments on a FAQ post. Only the author of the comment
can edit it, and edited comments are marked as pending approval.
"""


@method_decorator(login_required, name='dispatch')
class FAQCommentEdit(View):
    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return HttpResponseForbidden()

        try:
            data = json.loads(request.body)
            form = CommentForm(data, instance=comment)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'})

        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = False  # Mark as pending approval
            comment.pending_approval = True
            comment.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Form is not valid.'})


"""
Handles deletion of a comment on a FAQ post. Only the author of the comment
can delete it.
"""


@login_required
def delete_faq_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return HttpResponseForbidden()
    comment.delete()
    return JsonResponse({'success': True})
