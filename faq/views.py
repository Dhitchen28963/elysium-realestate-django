from django.views.generic import ListView
from .models import FAQ

class FAQListView(ListView):
    model = FAQ
    template_name = 'faq/faq_list.html'
    context_object_name = 'faqs'
