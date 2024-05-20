from django.urls import path
from .views import PropertyGuideListView

urlpatterns = [
    path('', PropertyGuideListView.as_view(), name='property_guide_list'),
]
