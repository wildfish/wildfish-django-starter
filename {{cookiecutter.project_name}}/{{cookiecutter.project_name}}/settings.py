from os import environ
from pathlib import Path

import envdir
import sentry_sdk
from configurations import Configuration
from sentry_sdk.integrations.django import DjangoIntegration


# Common settings
BASE_DIR = Path(__file__).absolute().parent.parent
PROJECT_NAME = "{{cookiecutter.project_name}}"
CONFIGURATION = environ["DJANGO_CONFIGURATION"]
CONFIG_DIR = environ.get("DJANGO_CONFIG_DIR")
SECRET_DIR = environ.get("DJANGO_SECRET_DIR")

# Detect if we are running tests.
IN_TESTS = environ.get("RUNNING_TESTS")


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


def get_secret(name, cast=str):
    """
    Get a secret from disk
    Secrets should be available as the content of `<SECRET_DIR>/<name>`
    All secrets are required
    Arguments:
        name (str): Name of environment variable
        cast (Callable): function to call on extracted string value
    """

    # We don't want this to be called unless we're in a configuration which uses it
    def _lookup(self):
        if not SECRET_DIR:
            raise ValueError(
                f"Secret {name} not found: DJANGO_SECRET_DIR not set in env"
            )

        file = Path(SECRET_DIR) / name
        if not file.exists():
            raise ValueError(f"Secret {file} not found")

        value = file.read_text().strip()
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


class Common(Configuration):
    @classmethod
    def pre_setup(cls):
        """
        If specified, add config dir to environment
        """
        if CONFIG_DIR:
            envdir.Env(CONFIG_DIR)
        super().pre_setup()

    PROJECT_ENVIRONMENT_SLUG = f"{PROJECT_NAME}_{CONFIGURATION}".lower()

    @property
    def ADMINS(self):
        """
        Look up DJANGO_ADMINS and split into list of (name, email) tuples
        Separate name and email with commas, name+email pairs with semicolons, eg::
            DJANGO_ADMINS="User One,user1@example.com;User Two,user2@example.com"
        """
        value = environ.get("DJANGO_ADMINS")
        if not value:
            return []

        pairs = value.split(";")
        return [pair.rsplit(",", 1) for pair in pairs]

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
    ]

    ROOT_URLCONF = "{{cookiecutter.project_name}}.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
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
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    DATABASE_HOST = get_env("DATABASE_HOST", default="localhost")
    DATABASE_PORT = get_env("DATABASE_PORT", default=5432, cast=int)
    DATABASE_NAME = get_env("DATABASE_NAME", default=PROJECT_NAME)
    DATABASE_USER = get_env("DATABASE_USER", default=PROJECT_NAME)
    DATABASE_PASSWORD = get_env("DATABASE_PASSWORD", default=PROJECT_NAME)

    @property
    def DATABASES(self):
        """
        Build the databases object here to allow subclasses to override specific values
        """
        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "HOST": self.DATABASE_HOST,
                "PORT": self.DATABASE_PORT,
                "NAME": self.DATABASE_NAME,
                "USER": self.DATABASE_USER,
                "PASSWORD": self.DATABASE_PASSWORD,
            }
        }

    # Password validation
    # https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.0/topics/i18n/
    LANGUAGE_CODE = "en-GB"

    TIME_ZONE = "{{cookiecutter.time_zone}}"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "static"

    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

    # Additional locations of static files
    STATICFILES_DIRS = [BASE_DIR / "frontend" / "dist"]

    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_ROOT = BASE_DIR / "public"

    FIXTURE_DIRS = [BASE_DIR / "fixtures"]

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            },
        },
        "handlers": {"console": {"class": "logging.StreamHandler"}},
        "loggers": {
            "django": {"handlers": ["console"], "level": "INFO"},
            "sentry_sdk": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }


class RedisCache:
    REDIS_HOST = get_env("DJANGO_REDIS_HOST", required=True)
    REDIS_PORT = get_env("DJANGO_REDIS_PORT", default=6379, cast=int)

    # Cache
    # https://docs.djangoproject.com/en/3.0/ref/settings/#caches
    @property
    def CACHES(self):
        return {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1",
                "KEY_PREFIX": f"{self.PROJECT_ENVIRONMENT_SLUG}_",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    "PARSER_CLASS": "redis.connection.HiredisParser",
                },
            }
        }


class Dev(Common):
    DEBUG = True
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = "/tmp/app-emails"
    INTERNAL_IPS = ["127.0.0.1"]

    @property
    def INSTALLED_APPS(self):
        INSTALLED_APPS = super().INSTALLED_APPS
        INSTALLED_APPS.append("debug_toolbar")
        return INSTALLED_APPS

    @property
    def MIDDLEWARE(self):
        MIDDLEWARE = super().MIDDLEWARE
        MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
        return MIDDLEWARE


class DevDocker(RedisCache, Dev):
    """
    Dev for docker, uses Redis.
    """


class Test(Common):
    """
    Default test settings

    Includes some testing speedups.
    """

    DEBUG = False
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


class CI(Test):
    """
    Default CI settings
    """


class Deployed(RedisCache, Common):
    """
    Settings which are for a non-local deployment
    """

    # Redefine values which are not optional in a deployed environment
    ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS", cast=csv_to_list, required=True)

    # Some deployed settings are no longer env vars - collect from the secret store
    SECRET_KEY = get_secret("DJANGO_SECRET_KEY")
    DATABASE_USER = get_secret("DATABASE_USER")
    DATABASE_PASSWORD = get_secret("DATABASE_PASSWORD")

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

    # django-debug-toolbar will throw an ImproperlyConfigured exception if DEBUG is
    # ever turned on when run with a WSGI server
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = "{{cookiecutter.email_user}}"
    EMAIL_HOST_PASSWORD = "{{cookiecutter.email_password}}"
    DEFAULT_FROM_EMAIL = ""
    SERVER_EMAIL = ""

    @classmethod
    def post_setup(cls):
        super(Deployed, cls).post_setup()
        sentry_sdk.init(
            dsn="{{cookiecutter.sentry_dsn}}",
            integrations=[DjangoIntegration()],
            environment=CONFIGURATION,
        )


class Stage(Deployed):
    pass


class Prod(Deployed):
    DEBUG = False
