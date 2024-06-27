import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.conf import settings
import logging

logging.basicConfig(level=logging.DEBUG)

# Set up retry strategy for requests
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def send_email_via_emailjs(to_email, subject, message, to_name, from_name, from_email, property_title):
    url = 'https://api.emailjs.com/api/v1.0/email/send'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.EMAILJS_PRIVATE_KEY}'  # Include the private key
    }
    data = {
        'service_id': settings.EMAILJS_SERVICE_ID,
        'template_id': settings.EMAILJS_CONTACT_FORM_TEMPLATE_ID,  # Use contact form template
        'user_id': settings.EMAILJS_USER_ID,
        'template_params': {
            'to_email': to_email,
            'subject': subject,
            'message': message,
            'to_name': to_name,
            'from_name': from_name,
            'from_email': from_email,
            'property_title': property_title,
        },
    }

    logging.debug(f"URL: {url}")
    logging.debug(f"Headers: {headers}")
    logging.debug(f"Data: {data}")
    logging.debug(f"Private key explicitly: {settings.EMAILJS_PRIVATE_KEY}")

    response = http.post(url, headers=headers, json=data)
    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Text: {response.text}")
    return response.status_code, response.text