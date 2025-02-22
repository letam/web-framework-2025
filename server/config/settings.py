"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.2.2.

Note: The doc reference URLs to djangoproject.com in project have been updated
to reflect the latest version of Django used in the project--currently 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import environ
import os
from pathlib import Path


# Environment variables
# Reference: https://github.com/joke2k/django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IS_RUNNING_FROM_PROJECT_ROOT = \
    Path(BASE_DIR / 'server').exists()

ENV_FILE = 'server/.env'

if IS_RUNNING_FROM_PROJECT_ROOT and not Path(ENV_FILE).is_file():
    print('Required .env file not found.')
    from django.core.management.utils import get_random_secret_key
    with open(ENV_FILE, 'a') as f:
        f.write('DEBUG=True\n')
        f.write('SECRET_KEY=' + get_random_secret_key() + '\n')
        f.write('DATABASE_URL=sqlite:///server/db.sqlite3\n')
    print('Created .env file at server/.env with default values for development.')
    print('WARNING: Please edit the .env file for production environment.')
    print()

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start settings
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
        'webframework.app',
        'dev.webframework.app',
    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    # third-party apps
    'rest_framework',
    'corsheaders',
    'django_extensions',

    # project apps
    'apps.users.apps.UsersConfig',
    'apps.website',
    'apps.blogs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': env.db() or {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 16,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging
# https://docs.djangoproject.com/en/5.1/topics/logging/
import copy
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)


def setup_save_errorlog_to_file(logging: dict):
    import os

    log_dir: Path = BASE_DIR / '..' / 'log'
    errorlog_filepath: Path = log_dir / 'server-errors.log'

    def create_log_dir_for_server_errors():
        if not log_dir.exists():
            os.mkdir(log_dir)
        if not errorlog_filepath.exists():
            try:
                os.mknod(errorlog_filepath)
            except PermissionError:
                with open(errorlog_filepath, 'w'):
                    pass

    create_log_dir_for_server_errors()

    # if not DEBUG:
    #     # In case of a single server managing multiple apps, symlink the project's server error log to the common /var/log/app-errors directory
    #     def symlink_error_log_in_system_logs():
    #         log_symlinkpath: str = f'/var/log/app-errors/{BASE_DIR.parent.name}.log'
    #         if not Path(log_symlinkpath).parent.exists():
    #             import subprocess

    #             subprocess.call('./sys/mkdir-error-log')
    #             # subprocess.call(BASE_DIR / '..' / 'sys/mkdir-error-log')
    #         if not Path(log_symlinkpath).is_symlink():
    #             os.symlink(errorlog_filepath, log_symlinkpath)

    #     try:
    #         symlink_error_log_in_system_logs()
    #     except FileNotFoundError as e:
    #         print(e)

    logging['handlers'].update(
        {
            'file_errors': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'formatter': 'django.server',
                'class': 'logging.FileHandler',
                'filename': errorlog_filepath,
            },
        }
    )
    logging['loggers']['django']['handlers'].append('file_errors')
    return logging


LOGGING = setup_save_errorlog_to_file(LOGGING)


# User Model
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
AUTH_USER_MODEL = 'users.User'


# REST Framework
# https://www.django-rest-framework.org/#example
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Handle server headers required for Cross-Origin Resource Sharing (CORS)
# https://pypi.org/project/django-cors-headers/
CORS_ALLOWED_ORIGINS = [
    # 'http://localhost:8080',
    # 'http://127.0.0.1:9000'
]
if DEBUG:
    CORS_ALLOWED_ORIGINS.extend(
        [
            'http://localhost:3000',
            'http://localhost:5173',
            'http://127.0.0.1:5173',
        ]
    )
else:
    CORS_ALLOWED_ORIGINS.extend(
        [
            'http://127.0.0.1:8000',
            'https://dev.webframework.app',
        ]
    )

# Set debug value in templates
# https://stackoverflow.com/questions/1271631/how-to-check-the-template-debug-flag-in-a-django-template
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']


# https://whitenoise.readthedocs.io/en/stable/django.html
STORAGES = {
    # ...
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


SERVER_PATH = Path.cwd() / 'server'

STATIC_ROOT = SERVER_PATH / 'static'
STATIC_URL = '/static/'

MEDIA_ROOT = SERVER_PATH / 'uploads'
MEDIA_URL = '/uploads/'