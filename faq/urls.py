from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.FAQList.as_view(), name='faq_list'),
    path('<slug:slug>/', views.FAQDetail.as_view(), name='faq_detail'),
    path('summernote/', include('django_summernote.urls')),
]
