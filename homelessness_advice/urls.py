from django.urls import path
from .views import HomelessnessAdviceListView, HomelessnessAdviceDetailView

urlpatterns = [
    path('', HomelessnessAdviceListView.as_view(), name='homelessness_advice_list'),
    path('<slug:slug>/', HomelessnessAdviceDetailView.as_view(), name='homelessness_advice_detail'),
]
