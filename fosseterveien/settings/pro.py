from .base import *

DEBUG = False

ADMINS = ((SECRETS["ADMIN"]["NAVN"], SECRETS["ADMIN"]["EPOST"]),)

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "NAME": SECRETS["DB_NAME"],
        "USER": SECRETS["DB_USER"],
        "PASSWORD": SECRETS["PASS"],
    }
}
