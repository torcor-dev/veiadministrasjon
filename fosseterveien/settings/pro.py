from .base import *

DEBUG = False

#SECURE_SSL_REDIRECT = True
#CSRF_COOKIE_SECURE = True

ADMINS = ((SECRETS["ADMIN"]["NAVN"], SECRETS["ADMIN"]["EPOST"]),)

ALLOWED_HOSTS = [SECRETS["HOSTS"]["SUB"]]

INSTALLED_APPS.append("django.contrib.postgres")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "NAME": SECRETS["DB_NAME"],
        "USER": SECRETS["DB_USER"],
        "PASSWORD": SECRETS["PASS"],
    }
}
