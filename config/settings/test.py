from .base import *  # noqa: F403
import environ

env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR) + "/.env")  # noqa: F405

SECRET_KEY = env('TEST_SECRET_KEY')
DEBUG = False

DATABASES = {
    "default": env.db('TEST_DATABASE_URL')
}

DEBUG_TOOLBAR_CONFIG = {
    'ENABLED': False,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
