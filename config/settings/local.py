from .base import *


DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Email settings for development: use Mailpit (local SMTP) on port 1025
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "xcheche31@gmail.com")
