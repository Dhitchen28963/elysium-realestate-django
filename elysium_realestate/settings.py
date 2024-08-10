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
    '8000-dhitchen289-elysiumreal-edmywjdr1el.ws.codeinstitute-ide.net',
    '.herokuapp.com'
]

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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

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

# SQLite for testing
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }

CSRF_TRUSTED_ORIGINS = [
    "https://*.gitpod.io",
    "https://*.herokuapp.com",
    "https://8000-dhitchen289-elysiumreal-edmywjdr1el.ws.codeinstitute-ide.net",
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

SUMMERNOTE_THEME = "bs4"

SUMMERNOTE_CONFIG = {
    'iframe': False,
    'summernote': {
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear', 'color']],
            ['fontsize', ['fontsize']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
        'fontNames': [
            'Arial', 'Arial Black', 'Comic Sans MS', 'Courier New',
            'Helvetica', 'Impact', 'Tahoma', 'Times New Roman',
            'Verdana', 'Roboto', 'Inconsolata'
        ],
        'fontSizes': ['8', '9', '10', '11', '12', '14', '18', '24', '36'],
        'fontsizeUnits': ['px', 'pt'],
    },
    'codemirror': {
        'mode': 'htmlmixed',
        'lineNumbers': True,
    },
    'css': {
        'all': [
            'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.css',
            'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.12/summernote-bs4.css',
        ],
    },
    'js': {
        'all': [
            'https://code.jquery.com/jquery-3.3.1.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
            'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.js',
            'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.12/summernote-bs4.min.js',
        ],
    },
}



