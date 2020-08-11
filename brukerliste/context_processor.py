from django.conf import settings


def site_admin(request):
    return {
        "admin": {
            "navn": settings.SECRETS["ADMIN"]["NAVN"],
            "epost": settings.SECRETS["ADMIN"]["EPOST"],
        }
    }
