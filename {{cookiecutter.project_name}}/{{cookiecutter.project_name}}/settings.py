from os import environ
from os.path import abspath, dirname, join
from sys import argv

import sentry_sdk
from configurations import Configuration
from sentry_sdk.integrations.django import DjangoIntegration


PROJECT_NAME = "{{cookiecutter.project_name}}"
CONFIGURATION = environ["DJANGO_CONFIGURATION"]

# Detect if we are running tests.  Is this really the best way?
IN_TESTS = "test" in argv


def get_env(name, default=None, required=False, cast=str):
    """
    Get an environment variable
    Arguments:
        name (str): Name of environment variable
        default (Any): default value
        required (bool): If True, raises an ImproperlyConfigured error if not defined
        cast (Callable): function to call with extracted string value.
            Not applied to defaults.
    """

    def _lookup(self):
        value = environ.get(name)

        if value is None and default is not None:
            return default

        if value is None and required:
            raise ValueError(f"{name} not found in env")

        return cast(value)

    return property(_lookup)


def csv_to_list(value):
    """
    Convert a comma separated list of values into a list.
    Convenience function for use with get_env() and get_secret() ``cast`` argument.
    """
    if value is None:
        return []
    return value.split(",")


class RedisCache(object):
    pass
    # CACHES = {
    #     "default": {
    #         "BACKEND": "django_redis.cache.RedisCache",
    #         "LOCATION": "redis://{}:{}/1".format(
    #             get_env("REDIS_SERVICE_HOST", "127.0.0.1"),
    #             get_env("REDIS_SERVICE_PORT", 6379),
    #         ),
    #         "KEY_PREFIX": "{}_".format(PROJECT_ENVIRONMENT_SLUG),
    #         "OPTIONS": {
    #             "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #             "PARSER_CLASS": "redis.connection.HiredisParser",
    #             # You may want this. See https://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
    #             # 'IGNORE_EXCEPTIONS': True, # see
    #         },
    #     }
    # }
    # SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    # SESSION_CACHE_ALIAS = "default"


class Common(Configuration):
    PROJECT_ENVIRONMENT_SLUG = f"{PROJECT_NAME}_{CONFIGURATION}".lower()
    BASE_DIR = dirname(dirname(abspath(__file__)))

    ADMINS = (("{{cookiecutter.author_name}}", "{{cookiecutter.author_email}}"),)

    MANAGERS = ADMINS

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = get_env("DJANGO_SECRET_KEY", PROJECT_NAME)

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS", cast=csv_to_list, default=["*"])

    INSTALLED_APPS = [
        # Django
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        # Third party
        "whitenoise.runserver_nostatic",
        "django.contrib.staticfiles",
        "debug_toolbar",
        "django_extensions",
        "clear_cache",
        # Project
        "{{cookiecutter.project_name}}.{{cookiecutter.app_name}}",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    ROOT_URLCONF = "{{cookiecutter.project_name}}.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [join(BASE_DIR, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "{{cookiecutter.project_name}}.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": join(BASE_DIR, "db.sqlite3"),
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/
    LANGUAGE_CODE = "en-GB"

    TIME_ZONE = "{{cookiecutter.time_zone}}"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.11/howto/static-files/
    STATIC_URL = "/static/"
    STATIC_ROOT = join(BASE_DIR, "static_root")

    MEDIA_URL = "/media/"
    MEDIA_ROOT = join(BASE_DIR, "media")

    # Additional locations of static files
    STATICFILES_DIRS = [
        join(BASE_DIR, "static"),
    ]

    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    FIXTURE_DIRS = [join(BASE_DIR, "fixtures")]


class Dev(Common):
    DEBUG = True
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = "/tmp/app-emails"
    INTERNAL_IPS = [
        "127.0.0.1",
    ]


class Test(Dev):
    """
    Default test settings
    """

    DEBUG = False


class Deployed(RedisCache, Common):
    """
    Settings which are for a non local deployment, served behind nginx.
    """

    # django-debug-toolbar will throw an ImproperlyConfigured exception if DEBUG is
    # ever turned on when run with a WSGI server
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    PUBLIC_ROOT = join(Common.BASE_DIR, "../public/")
    STATIC_ROOT = join(PUBLIC_ROOT, "static")
    MEDIA_ROOT = join(PUBLIC_ROOT, "media")
    COMPRESS_OUTPUT_DIR = ""

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = "{{cookiecutter.email_user}}"
    EMAIL_HOST_PASSWORD = "{{cookiecutter.email_password}}"
    DEFAULT_FROM_EMAIL = ""
    SERVER_EMAIL = ""

    ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS", cast=csv_to_list, required=True)

    @classmethod
    def post_setup(cls):
        super(Deployed, cls).post_setup()
        sentry_sdk.init(
            dsn="{{cookiecutter.sentry_dsn}}", integrations=[DjangoIntegration()],
        )


class Stage(Deployed):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": get_env("POSTGRES_USER", ""),
            "USER": get_env("POSTGRES_USER", ""),
            "PASSWORD": get_env("POSTGRES_PASSWORD", "password"),
            "HOST": get_env("POSTGRES_SERVICE_HOST", "localhost"),
        }
    }


class Prod(Deployed):
    DEBUG = False

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": get_env("POSTGRES_USER", ""),
            "USER": get_env("POSTGRES_USER", ""),
            "PASSWORD": get_env("POSTGRES_PASSWORD", "password"),
            "HOST": get_env("POSTGRES_SERVICE_HOST", "localhost"),
        }
    }
