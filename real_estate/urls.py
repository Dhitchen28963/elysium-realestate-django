from . import views
from django.urls import path

urlpatterns = [
    path('', views.PropertyList.as_view(), name='home'),
]