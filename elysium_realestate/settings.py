import os
import dj_database_url
import sys

if os.path.isfile('env.py'):
    import env

# Basic settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
ALLOWED_HOSTS += [
    '8000-dhitchen289-elysiumreal-55uquhghxlj.ws.codeinstitute-ide.net',
    '.herokuapp.com',
]

# Cloudinary configuration
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'csp',
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

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# CSP Settings
CSP_DEFAULT_SRC = ("'self'",)

CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    'https://code.jquery.com',
    'https://stackpath.bootstrapcdn.com',
    'https://cdnjs.cloudflare.com',
)

CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'https://cdnjs.cloudflare.com',
    'https://stackpath.bootstrapcdn.com',
    'https://fonts.googleapis.com',
    'https://use.fontawesome.com',
)

CSP_IMG_SRC = (
    "'self'",
    'https://res.cloudinary.com',
)

CSP_FONT_SRC = (
    "'self'",
    'https://fonts.gstatic.com',
    'https://use.fontawesome.com',
)

CSP_FRAME_SRC = ("'self'",)

# Force HTTPS redirects
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
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
                'real_estate.context_processors.viewing_slots',
            ],
        },
    },
]

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

# Update the default database if DATABASE_URL is set
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

# SQLite for testing
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }

CSRF_TRUSTED_ORIGINS = [
    "https://*.gitpod.io",
    "https://*.herokuapp.com",
    (
        "https://8000-dhitchen289-elysiumreal-edmywjdr1el"
        ".ws.codeinstitute-ide.net"
    ),
]

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

# Security settings
X_FRAME_OPTIONS = 'SAMEORIGIN'

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
