import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.parent / 'infra' / '.env')

SECRET_KEY = os.getenv('DJANGO_KEY')

DEBUG = int(os.getenv(key='DEBUG', default='0'))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='').split()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'application.apps.ApplicationConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'rest_framework',
    'djoser',
    'drf_yasg',
    'corsheaders',
    'django_prometheus'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware'
]

ROOT_URLCONF = 'service.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'

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

WSGI_APPLICATION = 'service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv(key='DB_ENGINE', default='django_prometheus.db.backends.postgresql'),
        'NAME': os.getenv(key='POSTGRES_DB', default='db_name'),
        'USER': os.getenv(key='POSTGRES_USER', default='db_user'),
        'PASSWORD': os.getenv(key='POSTGRES_PASSWORD', default='db_password'),
        'HOST': os.getenv(key='DB_HOST', default='db_host'),
        'PORT': os.getenv(key='DB_PORT', default='db_port')
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = os.getenv(key='TIME_ZONE', default='Asia/Yekaterinburg')

USE_I18N = True

USE_TZ = False

STATIC_ROOT = BASE_DIR / 'static'

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

DJOSER = {
    # Use custom serializers instead of standard djoser serializers
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
    }
}

AUTH_USER_MODEL = 'users.User'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default_handler': {
            'level': os.getenv(key='DEFAULT_HANDLER_LEVEL', default='DEBUG'),
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'default_formatter',
        },
        'request_handler': {
            'level': os.getenv(key='REQUEST_HANDLER_LEVEL', default='DEBUG'),
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        '': {
            'level': os.getenv(key='DEFAULT_LOGGER_LEVEL', default='DEBUG'),
            'filters': ['add_ip_address'],
            'handlers': ['default_handler']
        },
        'django.request': {
            'level': os.getenv(key='REQUEST_LOGGER_LEVEL', default='DEBUG'),
            'filters': ['add_ip_address'],
            'handlers': ['request_handler'],
            'propagate': False  # to avoid duplicates in the log
        },
    },
    'filters': {
        'add_ip_address': {
            '()': 'core.logging_extension.IPAddressFilter'
        }
    },
    'formatters': {
        'default_formatter': {
            'format': '[{levelname}] From: {ip} / {method} - {name} - {asctime} - {module} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

CORS_ALLOW_ALL_ORIGINS = bool(os.getenv(key='CORS_ALLOW_ALL_ORIGINS', default=''))

CORS_ALLOWED_ORIGINS = os.getenv(key='CORS_ALLOWED_ORIGINS', default='').split()
