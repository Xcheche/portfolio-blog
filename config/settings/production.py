from .base import *


DATABASES = {
	"default": {
		"ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
		"NAME": os.getenv("DB_NAME", "portfolio_blog_db"),
		"USER": os.getenv("DB_USER", "postgres"),
		"PASSWORD": os.getenv("DB_PASSWORD", "password"),
		"HOST": os.getenv("DB_HOST", "db"),
		"PORT": os.getenv("DB_PORT", "5432"),
	}
}

# If using a managed Postgres (Neon, etc.) you may want to pass SSL options
# via environment variables. This keeps credentials/configuration out of the code.
ssl_mode = os.getenv("DB_SSLMODE", "")
if ssl_mode:
    DATABASES["default"].setdefault("OPTIONS", {})["sslmode"] = ssl_mode
    ssl_root = os.getenv("DB_SSLROOTCERT")
    if ssl_root:
        DATABASES["default"]["OPTIONS"]["sslrootcert"] = ssl_root


# Security settings for production; read from environment to allow local dev without HTTPS.
# When deploying to production, set these env vars to enable HTTPS enforcement.
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False") == "True"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "False") == "True"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False") == "True"
USE_X_FORWARDED_HOST = os.getenv("USE_X_FORWARDED_HOST", "True") == "True"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")