from .base import *  # noqa: F403

environ.Env.read_env(env_file=str(BASE_DIR) + "/.env")  # noqa: F405

# Quick-start development settings - unsuitable for production
SECRET_KEY = env("SECRET_KEY")  # noqa: F405
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": env.db(),  # noqa: F405
}

STORAGES = {
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    }
}

INSTALLED_APPS.insert(-1, 'debug_toolbar')  # noqa: F405
MIDDLEWARE.insert(-1, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
