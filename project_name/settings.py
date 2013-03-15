from os.path import abspath, basename, dirname, join
from configurations import Settings

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
SITE_NAME = basename(PROJECT_ROOT)


class Base(Settings):
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
        'django_jenkins',
        'raven.contrib.django',
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

    TEST_RUNNER = 'discover_runner.DiscoverRunner'

    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
    INTERNAL_IPS = ('127.0.0.1',)


class Development(Base):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG


class Staging(Base):
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


class Production(Base):
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
