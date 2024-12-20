from .base import *


SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

DATABASES = {
    "default": env.db(),
}

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        "BACKEND": 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
