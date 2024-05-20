from django.views.generic import ListView, DetailView
from .models import FAQ

class FAQListView(ListView):
    model = FAQ
    template_name = 'faq/faq_list.html'

class FAQDetailView(DetailView):
    model = FAQ
    template_name = 'faq/faq_detail.html'
