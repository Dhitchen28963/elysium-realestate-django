from django.urls import path, include
from .views import HomelessList, HomelessDetail

urlpatterns = [
    path('', HomelessList.as_view(), name='homelessness_advice_list'),
    path(
        '<slug:slug>/', HomelessDetail.as_view(),
        name='homelessness_advice_detail'
    ),
]
