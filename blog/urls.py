from django.urls import path, include
from .views import BlogList, BlogDetail, BlogCommentEdit, delete_blog_comment

urlpatterns = [
    path('', BlogList.as_view(), name='blog_list'),
    path('<slug:slug>/', BlogDetail.as_view(), name='blog_detail'),
    path('comment/<int:comment_id>/edit/', BlogCommentEdit.as_view(), name='blog_comment_edit'),
    path('comment/<int:comment_id>/delete/', delete_blog_comment, name='blog_comment_delete'),
]
