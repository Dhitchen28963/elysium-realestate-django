from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactForm

"""
Handles the contact form submission. If the request method is POST, the form
is validated and, if valid, the data is saved. A JSON response is returned
indicating success or failure. If the request method is GET, an empty form is
displayed in the contact page.
"""


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data by saving it to the database
            form.save()
            return JsonResponse({'success': True})
        else:
            # Return errors if the form is invalid
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Display an empty form for GET requests
        form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form})
