from django.urls import path, include
from .views import FAQList, FAQDetail, FAQCommentEdit, delete_faq_comment

urlpatterns = [
    path('', FAQList.as_view(), name='faq_list'),
    path(
        '<slug:slug>/',
        FAQDetail.as_view(),
        name='faq_detail'
    ),
    path(
        'comment/<int:comment_id>/edit/',
        FAQCommentEdit.as_view(),
        name='faq_comment_edit'
    ),
    path(
        'comment/<int:comment_id>/delete/',
        delete_faq_comment,
        name='faq_comment_delete'
    ),
]
