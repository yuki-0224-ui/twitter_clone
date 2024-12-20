from .base import *

environ.Env.read_env(env_file=str(BASE_DIR) + "/.env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": env.db(),
}

STORAGES = {
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    }
}

INSTALLED_APPS.insert(-1, 'debug_toolbar')
MIDDLEWARE.insert(-1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1', ]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
