from django.urls import path
from .views import PropertyGuidesListView, PropertyGuidesDetailView

urlpatterns = [
    path('', PropertyGuidesListView.as_view(), name='property_guides_list'),
    path('<slug:slug>/', PropertyGuidesDetailView.as_view(), name='property_guides_detail'),
]
