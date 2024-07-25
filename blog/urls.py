from django.urls import path, include
from .views import PostList, PostDetail, CommentEdit, delete_comment

urlpatterns = [
    path('', PostList.as_view(), name='blog_list'),
    path('<slug:slug>/', PostDetail.as_view(), name='blog_detail'),
    path('comment/<int:comment_id>/edit/', CommentEdit.as_view(), name='comment_edit'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='comment_delete'),
    path('summernote/', include('django_summernote.urls')),
]
