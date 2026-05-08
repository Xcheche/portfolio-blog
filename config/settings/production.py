from .base import *

import dj_database_url


DEBUG = False

database_url = os.getenv("DATABASE_URL", "")

if database_url:
	DATABASES = {
		"default": dj_database_url.parse(
			database_url,
			conn_max_age=int(os.getenv("DB_CONN_MAX_AGE", "600")),
			ssl_require=os.getenv("DB_SSLMODE", "require") == "require",
		)
	}
else:
	DATABASES = {
		"default": {
			"ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
			"NAME": os.getenv("DB_NAME", ""),
			"USER": os.getenv("DB_USER", ""),
			"PASSWORD": os.getenv("DB_PASSWORD", ""),
			"HOST": os.getenv("DB_HOST", ""),
			"PORT": os.getenv("DB_PORT", "5432"),
		}
	}

# If using a managed Postgres (Neon, etc.) you may want to pass SSL options
# via environment variables. This keeps credentials/configuration out of the code.
ssl_mode = os.getenv("DB_SSLMODE", "")
if ssl_mode and not database_url:
    DATABASES["default"].setdefault("OPTIONS", {})["sslmode"] = ssl_mode
    ssl_root = os.getenv("DB_SSLROOTCERT")
    if ssl_root:
        DATABASES["default"]["OPTIONS"]["sslrootcert"] = ssl_root


# Security settings for production.
# Configure HTTPS, HSTS, and cookie security via your deployment platform
# (e.g., nginx, Gunicorn, or your hosting provider) rather than Django settings.
USE_X_FORWARDED_HOST = os.getenv("USE_X_FORWARDED_HOST", "True") == "True"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")