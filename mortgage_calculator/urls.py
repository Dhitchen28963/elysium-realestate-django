from django.urls import path
from .views import mortgage_calculator_view

urlpatterns = [
    path('', mortgage_calculator_view, name='mortgage_calculator'),
]