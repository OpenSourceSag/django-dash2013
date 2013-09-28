from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE = {
    'default':{
        'ENGINE': 'django.db.backends.postgresl_psycopg2',
        'NAME': 'agilebord',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}


