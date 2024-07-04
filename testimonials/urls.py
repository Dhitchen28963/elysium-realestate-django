from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='testimonials_list'),
    path('<int:id>/', views.PostDetail.as_view(), name='testimonials_detail'),
    path('summernote/', include('django_summernote.urls')),
]
