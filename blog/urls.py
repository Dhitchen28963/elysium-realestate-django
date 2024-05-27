from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='blog_list'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='blog_detail'),
]
