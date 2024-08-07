from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogList.as_view(), name='blog_list'),
    path('<slug:slug>/', views.BlogDetail.as_view(), name='blog_detail'),
    path('comment/edit/<int:comment_id>/', views.BlogCommentEdit.as_view(), name='comment_edit'),
    path('comment/delete/<int:comment_id>/', views.delete_blog_comment, name='comment_delete'),
]
