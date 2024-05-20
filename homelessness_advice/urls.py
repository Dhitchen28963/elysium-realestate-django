from django.urls import path
from .views import HomelessnessAdviceListView

urlpatterns = [
    path('', HomelessnessAdviceListView.as_view(), name='homelessness_advice_list'),
]
