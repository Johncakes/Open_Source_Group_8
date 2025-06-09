from config.settings.default import *  # noqa f403

DEBUG = False

ALLOWED_HOSTS = [os.environ.get("DJANGO_ALLOWED_HOST")]
