# from config.components.base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += ( # noqa
    'rangefilter',
    'debug_toolbar',
    'django_extensions',
    'corsheaders',
    'movies.apps.MoviesConfig',
)

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "corsheaders.middleware.CorsMiddleware",
] + MIDDLEWARE # noqa

LANGUAGE_CODE = 'ru-RU'

LOCALE_PATHS = ['movies/locale']

INTERNAL_IPS = ['127.0.0.1', ]

CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8082', ]
