from os import environ
from os.path import abspath, dirname, join
from sys import argv
from configurations import Configuration

BASE_DIR = dirname(dirname(abspath(__file__)))
PROJECT_NAME = '{{cookiecutter.project_name}}'
PROJECT_ENVIRONMENT_SLUG = '{}_{}'.format(PROJECT_NAME, environ.get('DJANGO_CONFIGURATION').lower())

# Detect if we are running tests.  Is this really the best way?
IN_TESTS = 'test' in argv


class RedisCache(object):
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '127.0.0.1:6379',
            'KEY_PREFIX': '{}_'.format(PROJECT_ENVIRONMENT_SLUG),
            'OPTIONS': {
                'DB': 1,
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            },
        },
    }


class Common(Configuration):
    ADMINS = (
        ('{{cookiecutter.author_name}}', '{{cookiecutter.author_email}}'),
    )

    MANAGERS = ADMINS

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '{{cookiecutter.secret_key}}'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'raven.contrib.django.raven_compat',
        'debug_toolbar',
        'bootstrap3',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'django_extensions',
        'clear_cache',
        '{{cookiecutter.project_name}}.accounts',
        '{{cookiecutter.project_name}}.{{cookiecutter.app_name}}',
    ]

    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    ROOT_URLCONF = '{{cookiecutter.project_name}}.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                join(BASE_DIR, 'templates')
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'allauth.account.context_processors.account',
                    'allauth.socialaccount.context_processors.socialaccount',
                ],
            },
        },
    ]

    WSGI_APPLICATION = '{{cookiecutter.project_name}}.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

    LANGUAGE_CODE = 'en-GB'

    TIME_ZONE = '{{cookiecutter.time_zone}}'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = join(BASE_DIR, 'static_root')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # Additional locations of static files
    STATICFILES_DIRS = [
        join(BASE_DIR, 'static'),
        join(BASE_DIR, 'bower_components'),
    ]

    FIXTURE_DIRS = [
        join(BASE_DIR, 'fixtures')
    ]

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    LOGIN_REDIRECT_URL = '/'

    SITE_ID = 1
    SITE_URL = 'http://localhost:8000/'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


class Dev(Common):
    DEBUG = True
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/app-emails'


class Deployed(RedisCache, Common):
    """
    Settings which are for a non local deployment, served behind nginx.
    """
    # django-debug-toolbar will throw an ImproperlyConfigured exception if DEBUG is
    # ever turned on when run with a WSGI server
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    PUBLIC_ROOT = join(BASE_DIR, '../public/')
    STATIC_ROOT = join(PUBLIC_ROOT, 'static')
    MEDIA_ROOT = join(PUBLIC_ROOT, 'media')
    COMPRESS_OUTPUT_DIR = ''

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = '{{cookiecutter.email_user}}'
    EMAIL_HOST_PASSWORD = '{{cookiecutter.email_password}}'
    DEFAULT_FROM_EMAIL = ''
    SERVER_EMAIL = ''


class Stage(Deployed):
    SITE_URL = 'http://stage.{{cookiecutter.domain_name}}'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
        }
    }


class Prod(Deployed):
    DEBUG = False

    SITE_URL = 'http://{{cookiecutter.domain_name}}'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
        }
    }

    ALLOWED_HOSTS = ['.{{cookiecutter.domain_name}}', ]  # add deployment domain here

    RAVEN_CONFIG = {
        'dsn': '{{cookiecutter.sentry_dsn}}'
    }
