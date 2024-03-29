import os

import django.core.mail.backends.smtp
import environ
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# Reading env
environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #! External
    'django_filters',
    'rest_framework',
    'debug_toolbar' ,
    'djoser',
    'drf_spectacular',
    'corsheaders',
    #? Internal
    'playground',
    'store',
    'tags',
    'likes',
    'core',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

#? CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:4357'
]

ROOT_URLCONF = 'Store_Pop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Store_Pop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DATABASE_NAME'),
        'USER': env('POSTGRES_USERNAME'),
        'PASSWORD': env('POSTGRES_PASSWORD')
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': ( 'rest_framework.permissions.AllowAny', ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

AUTH_USER_MODEL = 'core.User'

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'current_user': 'core.serializers.UserSerializer',
    }
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1)
}

# Swagger Doc schema
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    #? Permission
    # 'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAuthenticated'],
}

# SMTP
# Email Sending
#? When ever you wanted to change email sending method change after backends
# EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
CURRENT_SITE = env("CURRENT_SITE")
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'from@milad.com'

# For send_mail_admin
ADMINS = [
    ('milad', 'milad@gmail.com')
]

# import redis
#
# r = redis.Redis(
#   host='redis-11958.c290.ap-northeast-1-2.ec2.cloud.redislabs.com',
#   port=11958,
#   password='QucDkFJnj7avNcgjEPEwlG0FGWdqkOYr')

#* CELERY
CELERY_BROKER_URL = f"{env('CELERY_WORKER_PLATFORM')}{env('CELERY_WORKER_PLATFORM_PASSWORD')}{env('CELERY_WORKER_PLATFORM_URL')}"

# Schedule
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.main.notify_customers',
        #! 'schedule': 5 * 60 # Minutes
        'schedule': crontab(day_of_week = 1, hour = 7, minute = 30), # every monday at 7:30
        #? 'schedule': crontab(minute = '*/15') # every 15 minutes

        'args': ['Hello World'],
        # 'kwargs': {"id": 1}
    }
}