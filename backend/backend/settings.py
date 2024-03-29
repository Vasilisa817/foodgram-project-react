
import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', default='1234567890')

DEBUG = True

ALLOWED_HOSTS = [
    'backend:8000',
    '158.160.7.126:8000',
    'localhost',
    'backend',
    '158.160.7.126'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'colorfield',
    'users',
    'api',
    'recipes',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.CustomPagination',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('NAME', default='postgres'),
        'USER': os.getenv('USER', default='postgres'),
        'PASSWORD': os.getenv('PASSWORD', default='postgres'),
        'HOST': os.getenv('HOST', default='db'),
        'PORT': os.getenv('PORT', default='5432')
    }
}

AUTH_USER_MODEL = 'users.User'

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

DJOSER = {
    'SERIALIZERS': {
        'user': 'api.serializers.UsersManageSerializer',
        'user_create': 'api.serializers.CustomUserCreateSerializer',
        'current_user': 'api.serializers.UsersManageSerializer',
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMPTY = '-'


CORS_ORIGIN_WHITELIST = (
    'http://158.160.7.126:3000',
    'http://backend:3000',
    'http://localhost:3000',
)

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://testserver",
    "http://backend",
]
'''

import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', default='1234567890')

DEBUG = True

ALLOWED_HOSTS = [
    'backend:8000',
    '158.160.7.126:8000',
    'localhost',
    'backend',
    '158.160.7.126'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'colorfield',
    'users',
    'api',
    'recipes',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.CustomPagination',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('NAME', default='postgres'),
        'USER': os.getenv('USER', default='postgres'),
        'PASSWORD': os.getenv('PASSWORD', default='postgres'),
        'HOST': os.getenv('HOST', default='db'),
        'PORT': os.getenv('PORT', default='5432')
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

DJOSER = {
    'SERIALIZERS': {
        'user': 'api.serializers.UsersManageSerializer',
        'user_create': 'api.serializers.CustomUserCreateSerializer',
        'current_user': 'api.serializers.UsersManageSerializer',
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMPTY = '-'


CORS_URLS_REGEX = r'^/api/.*$'
CORS_ORIGIN_WHITELIST = (
    'http://158.160.7.126:3000',
    'http://backend:3000',
    'http://localhost:3000',
)

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://testserver",
    "http://backend",
]'''
