"""
Configuration Django — APOCAL'IPSSI 2026.

Lit les variables sensibles depuis `.env` via python-decouple.
La config se veut pédagogique : commentaires partout, sections clairement
séparées. Adaptez ce qui vous est utile.
"""
from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------------
# Sécurité
# ----------------------------------------------------------------------------
SECRET_KEY = config(
    "DJANGO_SECRET_KEY",
    default="dev-secret-key-change-me-in-production",
)
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="*", cast=Csv())

# ----------------------------------------------------------------------------
# Applications
# ----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Tiers
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    # Apps locales
    "accounts",
    "llm",
    "quizzes",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # avant CommonMiddleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "apocal.urls"
WSGI_APPLICATION = "apocal.wsgi.application"
ASGI_APPLICATION = "apocal.asgi.application"

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

# ----------------------------------------------------------------------------
# Base de données — Postgres via Docker
# ----------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME":     config("POSTGRES_DB",       default="apocal"),
        "USER":     config("POSTGRES_USER",     default="apocal"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="apocal-dev-only"),
        "HOST":     config("POSTGRES_HOST",     default="postgres"),
        "PORT":     config("POSTGRES_PORT",     default="5432"),
    }
}

# ----------------------------------------------------------------------------
# Validation mots de passe
# ----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------------------------------------------------------
# I18n
# ----------------------------------------------------------------------------
LANGUAGE_CODE = "fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------------------
# Statics
# ----------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------------------------------------------------------
# Django REST Framework
# ----------------------------------------------------------------------------
REST_FRAMEWORK = {
    # TokenAuthentication en premier : les requêtes du frontend (header
    # Authorization: Token ...) sont authentifiées par token, sans contrôle
    # CSRF. SessionAuthentication reste en second pour la navigation Swagger UI.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ----------------------------------------------------------------------------
# drf-spectacular (OpenAPI / Swagger)
# ----------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE":       "APOCAL'IPSSI 2026 — EduTutor IA API",
    "DESCRIPTION": "Plateforme de révision personnalisée à base de LLM. "
                   "Auth, génération de quiz, historique de progression.",
    "VERSION":     "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {
        "name": "Mohamed Amine EL AFRIT",
        "url":  "https://www.mohamedelafrit.com",
    },
    "LICENSE": {"name": "CC BY-NC-SA 4.0"},
}

# ----------------------------------------------------------------------------
# CORS (autorise le frontend Vite)
# ----------------------------------------------------------------------------
# Le port hôte du frontend est configurable via FRONTEND_HOST_PORT (.env) en
# cas de conflit sur le port 3000. On autorise dynamiquement ce port (en plus
# du 3000 par défaut) pour éviter tout blocage CORS. Surcharge totale possible
# en définissant CORS_ALLOWED_ORIGINS dans le .env (liste séparée par virgules).
_frontend_port = config("FRONTEND_HOST_PORT", default="3000")
_default_cors = {
    f"http://localhost:{_frontend_port}",
    f"http://127.0.0.1:{_frontend_port}",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
}
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default=",".join(sorted(_default_cors)),
    cast=Csv(),
)
CORS_ALLOW_CREDENTIALS = True

# ----------------------------------------------------------------------------
# Intégration LLM (Ollama)
# ----------------------------------------------------------------------------
# Fournisseur de génération de quiz. 4 valeurs possibles :
#   "ollama"    -> modèle LOCAL gratuit (défaut, recommandé en développement)
#   "openai"    -> API OpenAI (PAYANT, future version premium)
#   "anthropic" -> API Anthropic / Claude (PAYANT, future version premium)
#   "mock"      -> faux QCM instantanés (tests / dev sans LLM)
LLM_BACKEND  = config("LLM_BACKEND",  default="ollama")

# --- Ollama (local, gratuit) ---
OLLAMA_HOST  = config("OLLAMA_HOST",  default="http://ollama:11434")
OLLAMA_MODEL = config("OLLAMA_MODEL", default="llama3.1:8b")
# Délai max (secondes) d'attente d'une génération Ollama. Sur CPU, un modèle 8B
# met facilement 2 à 5 minutes pour 10 QCM : 120 s était trop court (timeout ->
# 502). Défaut généreux, ajustable via .env (OLLAMA_TIMEOUT).
OLLAMA_TIMEOUT = config("OLLAMA_TIMEOUT", default=600, cast=int)

# --- OpenAI (API payante) ---
# Laissez OPENAI_API_KEY vide en dev : le backend "openai" refusera de démarrer
# sans clé, ce qui est volontaire (évite les frais accidentels).
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
OPENAI_MODEL   = config("OPENAI_MODEL",   default="gpt-4o-mini")

# --- Anthropic / Claude (API payante) ---
ANTHROPIC_API_KEY = config("ANTHROPIC_API_KEY", default="")
ANTHROPIC_MODEL   = config("ANTHROPIC_MODEL",   default="claude-3-5-haiku-20241022")

# Délai max (secondes) pour les API cloud (OpenAI/Anthropic), bien plus rapides
# qu'un modèle local sur CPU.
LLM_API_TIMEOUT = config("LLM_API_TIMEOUT", default=60, cast=int)
