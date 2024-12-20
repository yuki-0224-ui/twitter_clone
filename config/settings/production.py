from .base import *  # noqa: F403

SECRET_KEY = env("SECRET_KEY")  # noqa: F405
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

DATABASES = {
    "default": env.db(),  # noqa: F405
}

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]  # noqa: F405

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        "BACKEND": 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),  # noqa: F405
    'API_KEY': env('CLOUDINARY_API_KEY'),  # noqa: F405
    'API_SECRET': env('CLOUDINARY_API_SECRET')  # noqa: F405
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # noqa: F405
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # noqa: F405
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')  # noqa: F405
