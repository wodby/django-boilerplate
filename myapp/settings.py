import json
import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() in {"1", "true", "yes"}
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be set when DJANGO_DEBUG is disabled."
        )
    SECRET_KEY = "development-only-secret-key"

LOOPBACK_HOSTS = ("localhost", "127.0.0.1", "[::1]")


def get_allowed_hosts(debug: bool) -> list[str]:
    """Build the host allowlist, including Wodby's loopback probe targets."""
    configured_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS")
    if configured_hosts:
        allowed_hosts = [
            host.strip() for host in configured_hosts.split(",") if host.strip()
        ]
    else:
        try:
            allowed_hosts = json.loads(os.environ.get("WODBY_HOSTS", "[]"))
        except json.JSONDecodeError as error:
            raise ImproperlyConfigured("WODBY_HOSTS must be a JSON array.") from error
        if not isinstance(allowed_hosts, list) or not all(
            isinstance(host, str) for host in allowed_hosts
        ):
            raise ImproperlyConfigured("WODBY_HOSTS must be a JSON array of hostnames.")

    wodby_service_host = os.environ.get("WODBY_APP_SERVICE_NAME")
    if wodby_service_host and wodby_service_host not in allowed_hosts:
        allowed_hosts.append(wodby_service_host)

    if os.environ.get("WODBY") and "*" not in allowed_hosts:
        allowed_hosts.extend(
            host for host in LOOPBACK_HOSTS if host not in allowed_hosts
        )

    if not allowed_hosts:
        return list(LOOPBACK_HOSTS) if debug else ["*"]
    return allowed_hosts


ALLOWED_HOSTS = get_allowed_hosts(DEBUG)

INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

ROOT_URLCONF = "myapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "myapp.wsgi.application"

if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=60,
            conn_health_checks=True,
        )
    }
elif os.environ.get("DB_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ.get("DB_PORT", "5432"),
            "NAME": os.environ.get(
                "DB_NAME", os.environ.get("DB_DATABASE", "postgres")
            ),
            "USER": os.environ.get("DB_USERNAME", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "CONN_MAX_AGE": 60,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

if os.environ.get("CELERY_BROKER_URL"):
    CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]

if os.environ.get("SMTP_HOST"):
    EMAIL_HOST = os.environ["SMTP_HOST"]
    EMAIL_PORT = int(os.environ.get("SMTP_PORT", "25"))
    EMAIL_TIMEOUT = 5

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
