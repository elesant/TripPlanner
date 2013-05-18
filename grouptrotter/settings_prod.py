from settings_base import *

ENVIRONMENT = 'PROD'

ALLOWED_HOSTS = [
    'grouptrotter.herokuapp.com',
]

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DAJAXICE_DEBUG = DEBUG

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'grouptrotter'
AWS_S3_FILE_OVERWRITE = True
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Cache-Control': 'public, max-age=%s' % (30 * 24 * 60 * 60),
}
COMPRESS_STORAGE = STATICFILES_STORAGE

STATIC_URL = 'https://s3.amazonaws.com/grouptrotter/'
MEDIA_URL = 'https://s3.amazonaws.com/grouptrotter/'

# Facebook Information
FACEBOOK_APP_ID = '132305200298528'
FACEBOOK_APP_SECRET = 'ac86a28d1b4209937fee5b16ed89baa7'

# AWS Information
AWS_ACCESS_KEY_ID = 'AKIAIWUXQY7UILQNXKDA'
AWS_SECRET_ACCESS_KEY = 'Mf/DGgaXrePLNS4M3bmBqLv9shUz/xH71PqqI4s9'

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'https://6c5c2f8ec9cd41abaf43c4179c49a7b7:b2c753b00ef44469a0e916d6bf3272c6@app.getsentry.com/8596',
}
