"""
Django settings for taskmanager project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = config("DEBUG", default=True, cast=bool)
SECRET_KEY = config("SECRET_KEY", default="unsafe-dev-key" if DEBUG else None)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Other apps...
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'django_extensions', #for showing all the urls python manage.py show_urls 
    # Our new app
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "taskmanager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "taskmanager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Step 4: Delete SQLite Database (Optional)
# If everything is working fine, you can remove the old db.sqlite3 file.
# rm db.sqlite3  # Linux/Mac
# del db.sqlite3  # Windows

#Postgres DataBase

#Using Environmen Variables
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("DB_NAME"),        
#         "USER": os.getenv("DB_USER"),        
#         "PASSWORD": os.getenv("DB_PASSWORD"), 
#         "HOST": os.getenv("DB_HOST"),        
#         "PORT": os.getenv("DB_PORT"),        
#     }
# }



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),        
        "USER": config("DB_USER"),        
        "PASSWORD": config("DB_PASSWORD"), 
        "HOST": config("DB_HOST", default="localhost"),        
        "PORT": config("DB_PORT", cast=int, default="5432"),        
    }
}

# Step 5: Backup Your PostggitreSQL Database
# It's always good to take a backup of your PostgreSQL database.

# pg_dump -U your_db_user -F c -b -v -f backup.dump your_db_name
# This creates a backup.dump file, which you can restore using:

# pg_restore -U your_db_user -d your_db_name backup.dump

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = "login"

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',  # Enables login in browsable API
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    #PAGINATION
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,  # Show 5 tasks per page

    # Rate Limiting (Throttle)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # 3 requests/min for anonymous users
        'rest_framework.throttling.UserRateThrottle',  # 5 requests/min for normal users
        'tasks.throttles.AdminRateThrottle',  # 10 requests/min for admins
    ],
    
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/minute',
        'user': '5/minute',
        'admin': '10/minute'  # Admin users get 10 requests/min
    }
    
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'admin_actions.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

APPEND_SLASH = False
# FASTAPI_AUTH_URL = "http://fastapi_auth_service:8001"
FASTAPI_AUTH_URL = os.getenv("FASTAPI_AUTH_URL")