from django.urls import path, include
from .views import valuation_view

urlpatterns = [
    path('', valuation_view, name='valuation'),
    path('summernote/', include('django_summernote.urls')),
]