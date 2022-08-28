import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mh%ka$du9=fj@+!lpvu^*5-&-so$5@mg&w9tbqdfo++h#y!azy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    # '51.250.100.63',
]


# Application definition

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
    'colorfield',
    'users.apps.UsersConfig',
    'djoser',
    'recipes.apps.RecipesConfig',
    'api.apps.ApiConfig',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_recipes.urls'

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

WSGI_APPLICATION = 'api_recipes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#     'default': {
#         'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
#         'NAME': os.getenv('DB_NAME', default='postgres'),
#         'USER': os.getenv('POSTGRES_USER', default='postgres'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
#         'HOST': os.getenv('DB_HOST', default='db'),
#         'PORT': os.getenv('DB_PORT')
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#             'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
#             'NAME': os.getenv('DB_NAME', default='postgres'),
#             'USER': os.getenv('POSTGRES_USER', default='postgres'),
#             'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
#             'HOST': os.getenv('DB_HOST', default='db'),
#             'PORT': os.getenv('DB_PORT')
#     }
# }


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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AUTHENTICATION_BACKENDS = (
#     # 'django_python3_ldap.auth.LDAPBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )
AUTH_USER_MODEL = 'users.User'


CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
DJOSER = {
    'HIDE_USERS': False,
    'PERMISSIONS': {
        # 'activation': ['rest_framework.permissions.AllowAny'],
        # 'password_reset': ['rest_framework.permissions.AllowAny'],
        # 'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        # 'set_password': ['rest_framework.permissions.CurrentUserOrAdmin'],
        # 'username_reset': ['rest_framework.permissions.AllowAny'],
        # 'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        # 'set_username': ['rest_framework.permissions.CurrentUserOrAdmin'],
        # 'user_create': ['rest_framework.permissions.AllowAny'],
        # 'user_delete': ['rest_framework.permissions.CurrentUserOrAdmin'],
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.AllowAny'],
        # 'token_create': ['rest_framework.permissions.AllowAny'],
        # 'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    },

    'SERIALIZERS': {
        'user': 'api.serializers.UserCustomSerializer',
        'current_user': 'api.serializers.UserCustomSerializer',
    },
}

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}




# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ],
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#     'DEFAULT_PAGINATION_CLASS':
#         'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,
#     'DEFAULT_FILTER_BACKENDS': [
#         'django_filters.rest_framework.DjangoFilterBackend'
#     ]
# }