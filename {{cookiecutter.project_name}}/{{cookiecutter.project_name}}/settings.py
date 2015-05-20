from os.path import dirname, join
from configurations import Configuration
from django.conf import global_settings

BASE_DIR = dirname(dirname(__file__))
PROJECT_NAME = '{{cookiecutter.project_name}}'


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


class Common(Configuration):
    ADMINS = (
        ('{{cookiecutter.author_name}}', '{{cookiecutter.author_email}}'),
    )

    MANAGERS = ADMINS

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '{{cookiecutter.secret_key}}'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'raven.contrib.django.raven_compat',
        'debug_toolbar',
        'bootstrap3',
        'django_extensions',
        'clear_cache',
        'pipeline',
        'rest_framework',
        '{{cookiecutter.project_name}}.{{cookiecutter.app_name}}',
    ]

    MIDDLEWARE_CLASSES = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    ROOT_URLCONF = '{{cookiecutter.project_name}}.urls'

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

    TEMPLATE_DIRS = [
        join(BASE_DIR, 'templates')
    ]

    FIXTURE_DIRS = [
        join(BASE_DIR, 'fixtures')
    ]

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

    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

    STATICFILES_FINDERS = global_settings.STATICFILES_FINDERS + ('pipeline.finders.PipelineFinder',)

    PIPELINE_COMPILERS = (
        'react.utils.pipeline.JSXCompiler',
    )

    PIPELINE_JS = {
        '{{cookiecutter.model_name|lower}}': {
            'source_filenames': [
                'js/{{cookiecutter.model_name|lower}}_grid.jsx',
            ],
            'output_filename': 'js/{{cookiecutter.model_name|lower}}.js'
        }
    }

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        ),
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.DjangoFilterBackend',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
        ),
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    }


class Dev(Common):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
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


class Prod(Deployed):
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

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

    ALLOWED_HOSTS = ['.{{cookiecutter.domain_name}}', ]  # add deployment domain here

    RAVEN_CONFIG = {
        'dsn': '{{cookiecutter.sentry_dsn}}'
    }
