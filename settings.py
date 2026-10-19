
"""
Configuration Django de La Casa da Festa Elisabeth.

Fichier situé directement à la racine du backend :
D:/projet/web/elisabeth_backend_corrige/settings.py
"""

from pathlib import Path
import os
from datetime import timedelta

from dotenv import load_dotenv


# ============================================================
# BASE DU PROJET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# CHARGEMENT DU FICHIER .ENV
# ============================================================

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True,
)


# ============================================================
# SÉCURITÉ
# ============================================================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-secret-change-me-before-production",
)

DEBUG = (
    os.getenv("DJANGO_DEBUG", "1").strip() == "1"
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "La Casa da Festa Elisabeth",
).strip()


# ============================================================
# APPLICATIONS DJANGO
# ============================================================

INSTALLED_APPS = [
    # Applications Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Applications tierces
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",

    # Application métier
    "application_elisabeth",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# ROUTES PRINCIPALES
# ============================================================

# urls.py se trouve directement à la racine du projet.
ROOT_URLCONF = "urls"


# ============================================================
# TEMPLATES
# ============================================================

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


# ============================================================
# WSGI / ASGI
# ============================================================

# Les fichiers wsgi.py et asgi.py sont à la racine du projet.
WSGI_APPLICATION = "wsgi.application"

ASGI_APPLICATION = "asgi.application"


# ============================================================
# BASE DE DONNÉES POSTGRESQL
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",

        "NAME": os.getenv(
            "PGDATABASE",
            "elisabeth_bdd",
        ),

        "USER": os.getenv(
            "PGUSER",
            "postgres",
        ),

        "PASSWORD": os.getenv(
            "PGPASSWORD",
            "billmamba2025",
        ),

        "HOST": os.getenv(
            "PGHOST",
            "127.0.0.1",
        ),

        "PORT": os.getenv(
            "PGPORT",
            "5432",
        ),
    }
}


# ============================================================
# INTERNATIONALISATION
# ============================================================

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = os.getenv(
    "TZ",
    "Africa/Kinshasa",
).strip()

USE_I18N = True

USE_TZ = True


# ============================================================
# FICHIERS STATIQUES
# ============================================================

STATIC_URL = "/static/"


# ============================================================
# FICHIERS MÉDIAS
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


# ============================================================
# CORS
# ============================================================

# Configuration adaptée au développement local.
# En production, limiter les origines aux domaines autorisés.
CORS_ALLOW_ALL_ORIGINS = DEBUG


# ============================================================
# JWT
# ============================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        hours=8,
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=30,
    ),
}


# ============================================================
# EMAIL / GMAIL
# ============================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = os.getenv(
    "EMAIL_HOST",
    "smtp.gmail.com",
).strip()

EMAIL_PORT = int(
    os.getenv(
        "EMAIL_PORT",
        "587",
    ).strip()
)

EMAIL_USE_TLS = (
    os.getenv(
        "EMAIL_USE_TLS",
        "True",
    )
    .strip()
    .lower()
    in ("true", "1", "yes")
)

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER",
    "",
).strip()

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD",
    "",
).strip()

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER,
).strip()


# ============================================================
# DESTINATAIRES EMAIL DES NOTIFICATIONS
# ============================================================

NOTIFICATION_EMAIL_TO = os.getenv(
    "NOTIFICATION_EMAIL_TO",
    "",
).strip()

ADMIN_NOTIFICATION_EMAILS = [
    email.strip()
    for email in NOTIFICATION_EMAIL_TO.split(",")
    if email.strip()
]


# ============================================================
# DESTINATAIRES WHATSAPP DES NOTIFICATIONS
# ============================================================

NOTIFICATION_WHATSAPP_TO = os.getenv(
    "NOTIFICATION_WHATSAPP_TO",
    "",
).strip()

ADMIN_NOTIFICATION_WHATSAPP = [
    number.strip()
    for number in NOTIFICATION_WHATSAPP_TO.split(",")
    if number.strip()
]


# ============================================================
# TWILIO WHATSAPP
# ============================================================

TWILIO_ACCOUNT_SID = os.getenv(
    "TWILIO_ACCOUNT_SID",
    "",
).strip()

TWILIO_AUTH_TOKEN = os.getenv(
    "TWILIO_AUTH_TOKEN",
    "",
).strip()

TWILIO_WHATSAPP_NUMBER = os.getenv(
    "TWILIO_WHATSAPP_NUMBER",
    "",
).strip()


# ============================================================
# CLÉ PRIMAIRE PAR DÉFAUT
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

