from os.path import abspath, basename, dirname, join
from configurations import Settings

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
SITE_NAME = basename(PROJECT_ROOT)


class RedisCache(object):
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '127.0.0.1:6379',
            'OPTIONS': {
                'DB': 1,
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            },
        },
    }


class Base(RedisCache, Settings):
    ADMINS = (
        # ('Your Name', 'your_email@example.com'),
    )

    MANAGERS = ADMINS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.sqlite',
        }
    }

    ALLOWED_HOSTS = []

    TIME_ZONE = 'Europe/London'
    LANGUAGE_CODE = 'en-GB'
    SITE_ID = 1

    MEDIA_ROOT = join(PROJECT_ROOT, 'media')
    MEDIA_URL = '/media/'
    STATIC_ROOT = join(PROJECT_ROOT, 'static_root')
    STATIC_URL = '/static/'

    # Additional locations of static files
    STATICFILES_DIRS = [
        join(PROJECT_ROOT, 'static')
    ]

    SECRET_KEY = '{{ secret_key }}'
    MIDDLEWARE_CLASSES = Settings.MIDDLEWARE_CLASSES + (
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    ROOT_URLCONF = '{{ project_name }}.urls'
    WSGI_APPLICATION = '{{ project_name }}.wsgi.application'
    TEMPLATE_DIRS = [
        join(PROJECT_ROOT, 'templates')
    ]

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'discover_runner',
        'django_jenkins',
        'raven.contrib.django.raven_compat',
        'debug_toolbar',
    ]

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    # Other Django settings
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

    FIXTURE_DIRS = [
        join(PROJECT_ROOT, 'fixtures')
    ]
    # App settings

    # django-jenkins
    PROJECT_APPS = [app for app in INSTALLED_APPS if app.startswith('{{ project_name }}.')]
    JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                     'django_jenkins.tasks.django_tests',
                     'django_jenkins.tasks.run_pep8',
                     'django_jenkins.tasks.with_coverage')

    # django-debug-toolbar
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
    INTERNAL_IPS = ('127.0.0.1',)


class Development(Base):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/app-emails'


class Deployed(object):
    """
    Settings which are for a non local deployment, served behind nginx.
    """
    PUBLIC_ROOT = join(PROJECT_ROOT, '../public/')
    STATIC_ROOT = join(PUBLIC_ROOT, 'static')
    MEDIA_ROOT = join(PUBLIC_ROOT, 'media')
    COMPRESS_OUTPUT_DIR = ''

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = ''
    SERVER_EMAIL = ''


class Staging(Deployed, Base):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'OPTIONS': {
                'autocommit': True,  # see https://docs.djangoproject.com/en/dev/ref/databases/#autocommit-mode
            }
        }
    }


class Production(Deployed, Base):
    DEBUG = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'OPTIONS': {
                'autocommit': True,  # see https://docs.djangoproject.com/en/dev/ref/databases/#autocommit-mode
            }
        }
    }

    ALLOWED_HOSTS = ['', ]  # add deployment domain here

    SENTRY_DSN = '<your sentry key>'  # add sentry DSN
