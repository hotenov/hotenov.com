"""Django settings for hotenov_com project."""
import mimetypes
import os
from pathlib import Path

from configurations import Configuration
from configurations import values
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class DjangoDefaults(Configuration):
    """Default Django 4 project template settings."""

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "django-insecure-%_%og($ppw35=u6_ew)rk15zu()j5k-hcknloiyq-_vcj=a!58"  # noqa: S105, E501,B950

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "default_dj.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
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

    WSGI_APPLICATION = "default_dj.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/4.2/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

    # yapf: disable
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501,B950
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501,B950
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501,B950
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501,B950
        },
    ]
    # yapf: enable

    # Internationalization
    # https://docs.djangoproject.com/en/4.2/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.2/howto/static-files/

    STATIC_URL = "static/"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


class BaseDjSettings(DjangoDefaults):
    """Base class for Django settings configuration."""

    # User can set LOCAL_ENV_FILE_PATH to change its default value
    # Default is './_DockerStuff/.env.dev.local'.
    # It can be either relative as default value (relative to repo root,
    # where 'src' and 'pyproject.toml' are located)
    # OR absolute (including Windows paths in double quotes)
    # File must contain two mandatory variables: SECRET_KEY and SQL_ENGINE
    if not os.environ.get("DOCKER_ENV_PATH", None):
        local_env_file = os.environ.get(
            "LOCAL_ENV_FILE_PATH",
            default="./_DockerStuff/.env.dev.local",
        )
        local_env_filepath = Path(local_env_file.strip('"'))
        if local_env_filepath.is_absolute():
            DOTENV = local_env_filepath.resolve()
        else:
            DOTENV = (BASE_DIR.parent / local_env_filepath).resolve()

    # COMMON SETTINGS FOR ANY ENVIRONMENT

    # The current site in the django_site database table
    SITE_ID = 1

    # In the .env file like: DJANGO_ROOT_URLCONF=my_django_project.urls
    ROOT_URLCONF = values.Value("my_django_project.urls")

    # In the .env file like:
    # DJANGO_WSGI_APPLICATION=my_django_project.wsgi.application
    WSGI_APPLICATION = values.Value("my_django_project.wsgi.application")

    # In the .env file like: DJANGO_TIME_ZONE=America/Chicago
    TIME_ZONE = values.Value("UTC")

    # In the .env file like: DJANGO_LANGUAGE_CODE=en
    LANGUAGE_CODE = values.Value("en-US")

    # A list of locations of additional static files
    STATICFILES_DIRS = [
        BASE_DIR / "static",  # common static dir for all apps
    ]

    # Folders where "general" .po / .mo files will be placed
    LOCALE_PATHS = [
        BASE_DIR / "locale",
    ]

    # DATABASE SETUP FROM ENV VARIABLES

    @classmethod
    def setup(cls):
        """Setup configuration class."""
        super().setup()

        # Create 'default' database with empty dictionary
        cls.DATABASES = dict(default={})

        cls.DATABASES["default"]["ENGINE"] = values.Value(
            "django.db.backends.sqlite3",
            environ_name="SQL_ENGINE",
            environ_prefix=None,
            environ_required=True,  # To avoid using SQLite during migration
        )

        cls.DATABASES["default"]["NAME"] = values.Value(
            BASE_DIR / "db.sqlite3",
            environ_name="SQL_DATABASE",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["USER"] = values.Value(
            "test_user",
            environ_name="SQL_USER",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["PASSWORD"] = values.Value(
            "password",
            environ_name="SQL_PASSWORD",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["HOST"] = values.Value(
            "localhost",
            environ_name="SQL_HOST",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["PORT"] = values.Value(
            "50400",
            environ_name="SQL_PORT",
            environ_prefix=None,
        )

    @property
    def PASSWORD_HASHERS(self):
        """Use 'scrypt' as default storage algorithm.

        By changing the order of PASSWORD_HASHERS.
        """
        # the first hasher in this list is the preferred algorithm.  any
        # password using different algorithms will be converted automatically
        # upon login
        hashers = list(Configuration.PASSWORD_HASHERS)
        # Shift last element to first position
        return hashers[-1:] + hashers[:-1]

    @property
    def INSTALLED_APPS(self):
        """Add apps to default list INSTALLED_APPS in Django 4."""
        top_apps = [
            "modeltranslation",
        ]
        default_apps = list(DjangoDefaults.INSTALLED_APPS)
        added_apps = [
            "django.contrib.sites",
            "django.contrib.flatpages",
            "django.contrib.sitemaps",
            "website.apps.WebsiteConfig",
            "resume.apps.ResumeConfig",
        ]
        return top_apps + default_apps + added_apps

    @property
    def MIDDLEWARE(self):
        """Add middlewares to default list MIDDLEWARE in Django 4."""
        # Get list of MIDDLEWARE from Django 4 default template
        modified_middleware = list(DjangoDefaults.MIDDLEWARE)
        # Insert 'LocaleMiddleware' after 'SessionMiddleware'
        modified_middleware.insert(
            modified_middleware.index(
                "django.contrib.sessions.middleware.SessionMiddleware"
            )
            + 1,
            "django.middleware.locale.LocaleMiddleware",
        )
        added_middleware = [
            "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
        ]
        return modified_middleware + added_middleware

    @property
    def TEMPLATES(self):
        """Change templates settings of default TEMPLATES in Django 4."""
        modified_templates = list(DjangoDefaults.TEMPLATES)
        # Add custom dirs to templates search
        modified_templates[0]["DIRS"] = [
            BASE_DIR / "templates",
        ]
        modified_templates[0]["OPTIONS"]["context_processors"].append(
            "website.context_processors.debug_flag"
        )
        return modified_templates

    # GENERAL SETTINGS FROM ENV FILE

    DEBUG = values.BooleanValue(True, environ_prefix=None)

    SECRET_KEY = values.SecretValue(environ_prefix=None)

    # ALLOWED_HOSTS should be a single string of hosts with a spaces.
    # In the .env file as (no DJANGO_ prefix! for now):
    # ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    ALLOWED_HOSTS = values.ListValue(
        ["localhost", "127.0.0.1", "[::1]"],
        separator=" ",
        environ_prefix=None,
    )

    # If you run 'frontend' client (as proxy)
    CSRF_TRUSTED_ORIGINS = values.ListValue(
        ["http://localhost:3000"],
        separator=" ",
        environ_prefix=None,
    )

    LANGUAGES = [
        ("en", _("English")),
        ("ru", _("Russian")),
    ]

    # Absolute path to the directory static files should be collected to.
    # Example: "/var/www/example.com/static/"
    # Repo root directory (parent of Django project folder 'src')
    # In the .env file like: DJANGO_STATIC_ROOT="/var/www/example.com/static/"
    STATIC_ROOT = values.Value(BASE_DIR / "staticfiles")

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Default is inside Django project folder (e.g. 'src/mediafiles')
    # In the .env file like: DJANGO_MEDIA_ROOT="/var/www/example.com/media/"
    MEDIA_ROOT = values.Value(BASE_DIR / "mediafiles")

    # URL that handles the media served from MEDIA_ROOT.
    # Examples: "http://example.com/media/", "http://media.example.com/"
    # In the .env file like: DJANGO_MEDIA_URL="media/"
    MEDIA_URL = values.Value("media/")

    # OWN SETTINGS

    # Default name will be the same as domain value
    DEFAULT_SITE_DOMAIN = values.Value("example.com", environ_prefix=None)

    # Custom sie name and domain
    SITE_NAME = values.Value("My Django Website", environ_prefix=None)
    SITE_DOMAIN = values.Value("my.example.com", environ_prefix=None)


class Dev(BaseDjSettings):
    """DEV environment specific settings."""

    # To serve JavaScript files in DEBUG (on Windows)
    mimetypes.add_type("application/javascript", ".js", True)


class StageDockerEnv(BaseDjSettings):
    """STAGE environment configuration within a Docker container."""

    STATIC_ROOT = values.SecretValue()

    MEDIA_ROOT = values.SecretValue()

    CSRF_COOKIE_SECURE = False

    SESSION_COOKIE_SECURE = False

    @property
    def MIDDLEWARE(self):
        """List of MIDDLEWARE without CSRF validation."""
        # Get list of MIDDLEWARE from 'BaseDjSetting' class
        modified_middleware = list(BaseDjSettings().MIDDLEWARE)
        # For test purpose remove CSRF validation from MIDDLEWARE
        modified_middleware.remove("django.middleware.csrf.CsrfViewMiddleware")
        return modified_middleware

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": False,
            },
        },
    }


class ProdEnv(StageDockerEnv):
    """Production environment configuration."""

    DEBUG = False

    MIDDLEWARE = BaseDjSettings().MIDDLEWARE

    CSRF_COOKIE_SECURE = True

    SESSION_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    @property
    def STORAGES(self):
        """Change backend type for staticfiles."""
        # Get default value of STORAGES from 'BaseDjSetting' class
        modified_storages = dict(BaseDjSettings.STORAGES)
        # Set 'ManifestStaticFilesStorage' (with MD5 hash in filenames)
        modified_storages["staticfiles"] = {
            "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"  # noqa: E501,B950
        }
        return modified_storages


class TestSettings(BaseDjSettings):
    """Settings configuration for pytest runner."""

    @classmethod
    def setup(cls):
        """Setup database credentials to run unit tests."""
        super().setup()

        cls.DATABASES["default"]["ENGINE"] = values.Value(
            "django.db.backends.sqlite3",
            environ_name="SQL_TEST_ENGINE",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["NAME"] = values.Value(
            BASE_DIR / "db.sqlite3",
            environ_name="SQL_TEST_DATABASE",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["USER"] = values.Value(
            "test_user",
            environ_name="SQL_TEST_USER",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["PASSWORD"] = values.Value(
            "password",
            environ_name="SQL_TEST_PASSWORD",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["HOST"] = values.Value(
            "localhost",
            environ_name="SQL_TEST_HOST",
            environ_prefix=None,
        )

        cls.DATABASES["default"]["PORT"] = values.Value(
            "50400",
            environ_name="SQL_TEST_PORT",
            environ_prefix=None,
        )
