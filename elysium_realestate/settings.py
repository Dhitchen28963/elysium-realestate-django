import os
import dj_database_url
import sys

if os.path.isfile('env.py'):
    import env

# Basic settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
ALLOWED_HOSTS += [
    '8000-dhitchen289-elysiumreal-edmywjdr1el.ws.codeinstitute-ide.net',
    '.herokuapp.com',
]

print("DEBUG:", DEBUG)
print("ALLOWED_HOSTS:", ALLOWED_HOSTS)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'cloudinary_storage',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_summernote',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap4',
    'contact',
    'home',
    'real_estate',
    'property_guides',
    'homelessness_advice',
    'blog',
    'faq',
    'mortgage_calculator',
]

print("INSTALLED_APPS:", INSTALLED_APPS)

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

print("MIDDLEWARE:", MIDDLEWARE)

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

print("TEMPLATES:", TEMPLATES)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'elysium_realestate.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quote_brink_crib_819211',
        'USER': 'uzssp4o3zbi',
        'PASSWORD': 'yEGDhPhl8zps',
        'HOST': (
            'ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech'
        ),
        'PORT': '5432',
    }
}

print("DATABASES['default']:", DATABASES['default'])

# Update the default database if DATABASE_URL is set
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    print("DATABASE_URL found, updating database configuration.")
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
    print("Updated DATABASES['default']:", DATABASES['default'])

# SQLite for testing
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
    print("Test environment detected, using SQLite:", DATABASES['default'])

CSRF_TRUSTED_ORIGINS = [
    "https://*.gitpod.io",
    "https://*.herokuapp.com",
    (
        "https://8000-dhitchen289-elysiumreal-edmywjdr1el"
        ".ws.codeinstitute-ide.net"
    ),
]

print("CSRF_TRUSTED_ORIGINS:", CSRF_TRUSTED_ORIGINS)

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

print("AUTH_PASSWORD_VALIDATORS:", AUTH_PASSWORD_VALIDATORS)

# Security settings
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

print("LANGUAGE_CODE:", LANGUAGE_CODE)
print("TIME_ZONE:", TIME_ZONE)

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

print("STATIC_URL:", STATIC_URL)
print("STATICFILES_DIRS:", STATICFILES_DIRS)
print("STATIC_ROOT:", STATIC_ROOT)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'