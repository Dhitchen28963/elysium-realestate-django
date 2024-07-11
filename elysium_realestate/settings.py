import os
import dj_database_url
import logging

if os.path.isfile('env.py'):
    import env

# Basic settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = ['8000-dhitchen289-elysiumreal-9k1yohn1y4v.ws.codeinstitute-ide.net', '.herokuapp.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_summernote',
    'cloudinary',
    'home',
    'real_estate',
    'property_guides',
    'homelessness_advice',
    'blog',
    'testimonials',
    'faq',
    'mortgage_calculator',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'elysium_realestate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'elysium_realestate.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quote_brink_crib_819211',
        'USER': 'uzssp4o3zbi',
        'PASSWORD': 'yEGDhPhl8zps',
        'HOST': 'ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech',
        'PORT': '5432',
    }
}

# Update the default database if DATABASE_URL is set
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

CSRF_TRUSTED_ORIGINS = [
    "https://*.gitpod.io",
    "https://*.herokuapp.com",
    "https://8000-dhitchen289-elysiumreal-9k1yohn1y4v.ws.codeinstitute-ide.net",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ACCOUNT_EMAIL_VERIFICATION = 'none'

# EmailJS settings
EMAILJS_SERVICE_ID = os.environ.get('EMAILJS_SERVICE_ID')
EMAILJS_CONTACT_FORM_TEMPLATE_ID = os.environ.get('EMAILJS_CONTACT_FORM_TEMPLATE_ID')
EMAILJS_CONTACT_REPLY_TEMPLATE_ID = os.environ.get('EMAILJS_CONTACT_REPLY_TEMPLATE_ID')
EMAILJS_USER_ID = os.environ.get('EMAILJS_USER_ID')
EMAILJS_PRIVATE_KEY = os.environ.get('EMAILJS_PRIVATE_KEY')
EMAILJS_PUBLIC_KEY = os.environ.get('EMAILJS_PUBLIC_KEY')

logging.debug(f"EMAILJS_SERVICE_ID: {EMAILJS_SERVICE_ID}")
logging.debug(f"EMAILJS_CONTACT_FORM_TEMPLATE_ID: {EMAILJS_CONTACT_FORM_TEMPLATE_ID}")
logging.debug(f"EMAILJS_CONTACT_REPLY_TEMPLATE_ID: {EMAILJS_CONTACT_REPLY_TEMPLATE_ID}")
logging.debug(f"EMAILJS_USER_ID: {EMAILJS_USER_ID}")
logging.debug(f"EMAILJS_PRIVATE_KEY: {EMAILJS_PRIVATE_KEY}")
logging.debug(f"EMAILJS_PUBLIC_KEY: {EMAILJS_PUBLIC_KEY}")

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'