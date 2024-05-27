from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='testimonials_list'),
    path('<int:id>/', views.PostDetail.as_view(), name='testimonials_detail'),
]
