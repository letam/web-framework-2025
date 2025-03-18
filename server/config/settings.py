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

# NOTE: In production container (Docker) image as well as gunicorn process, then the working directory is the project's server (Django project root) directory. Only during development and running the server from project root then we see the server child directory.
IS_SERVER_CHILD_DIR_PRESENT = (Path.cwd() / 'server').exists()
if IS_SERVER_CHILD_DIR_PRESENT:
    ENV_FILE = 'server/.env'
else:
    ENV_FILE = '.env'

if not Path(ENV_FILE).is_file():
    print('Required .env file not found.')
    from django.core.management.utils import get_random_secret_key
    with open(ENV_FILE, 'a') as f:
        f.write('SECRET_KEY=' + get_random_secret_key() + '\n')
        if IS_SERVER_CHILD_DIR_PRESENT:
            f.write('DEBUG=True\n')
            f.write('DATABASE_URL=sqlite:///server/db.sqlite3\n')
            f.write('USE_LOCAL_FILE_STORAGE=True\n')
            f.write('MEDIA_ROOT=server/uploads\n')
            print('Created .env file at server/.env with default values for development.')
            print('WARNING: Please edit the .env file for production environment.')
        else:
            f.write('DEBUG=False\n')
            f.write('DATABASE_URL=sqlite:////data/db.sqlite3\n')
            f.write('MEDIA_ROOT=/data/uploads\n')
            print('Created .env file at .env with default values for production.')
    print()

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start settings
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
# Also https://fly.io/django-beats/deploying-django-to-production/

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
        'FLY_APP_NAME.fly.dev',
        'webframework.fly.dev',
        'webframework.dev',
        'wut.sh',
        'www.wut.sh'
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
    'default': env.db(default='sqlite:///db.sqlite3') or {
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

SERVER_PATH = Path.cwd()
IS_SERVER_CHILD_DIR_PRESENT = (Path.cwd() / 'server').exists()
if IS_SERVER_CHILD_DIR_PRESENT:
    SERVER_PATH = SERVER_PATH / 'server'

STATIC_ROOT = SERVER_PATH / 'static'
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
        ]
    )

CSRF_TRUSTED_ORIGINS = [
    'https://FLY_APP_NAME.fly.dev',
    'https://webframework.fly.dev',
    'https://webframework.dev',
    'https://wut.sh',
    'https://www.wut.sh',
]

# Set debug value in templates
# https://stackoverflow.com/questions/1271631/how-to-check-the-template-debug-flag-in-a-django-template
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']


# File storage configuration
USE_LOCAL_FILE_STORAGE = os.getenv('USE_LOCAL_FILE_STORAGE', 'False').lower() == 'true'

# Configure Cloudflare R2 storage if not using local storage
if not USE_LOCAL_FILE_STORAGE:
    # Cloudflare R2 configuration
    AWS_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
    AWS_S3_ENDPOINT_URL = f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
    AWS_STORAGE_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'auto'  # R2 doesn't need a specific region
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False  # Don't add complex authentication-related query parameters to URLs

# Media files configuration
MEDIA_URL = env.str('MEDIA_URL', default='/media/')
MEDIA_ROOT = env.str('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'uploads'))

# Storage backend configuration
STORAGES = {
    # https://whitenoise.readthedocs.io/en/stable/django.html
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage' if USE_LOCAL_FILE_STORAGE else 'storages.backends.s3boto3.S3Boto3Storage',
    },
}

# Create uploads directory if using local storage
if USE_LOCAL_FILE_STORAGE and not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
