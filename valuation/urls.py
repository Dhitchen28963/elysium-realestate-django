from django.urls import path
from .views import valuation_view

urlpatterns = [
    path('', valuation_view, name='valuation'),
]