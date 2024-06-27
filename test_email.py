import os
import sys
import django
import logging

# Ensure the email_utils module can be found
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from real_estate.email_utils import send_email_via_emailjs

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elysium_realestate.settings')
django.setup()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Verify the environment variable
private_key = os.environ.get('EMAILJS_PRIVATE_KEY')
logging.debug(f"Using private key from environment variable: {private_key}")

# Test sending an email
try:
    logging.debug("Starting to send email...")
    status_code, response_text = send_email_via_emailjs(
        'hitchen28963@yahoo.com',
        'Test Email',
        'This is a test email using EmailJS.',
        'David Hitchen',  # to_name
        'Elysium Real Estate',  # from_name
        'hitchen28963@yahoo.com',  # from_email
        'Sample Property'  # property_title
    )
    logging.debug(f"Email sent successfully with status code {status_code}")
    print(f"Email sent successfully with status code {status_code}")
    print(f"Response: {response_text}")
except Exception as e:
    logging.error("An error occurred: %s", e)
    print(f"An error occurred: {e}")