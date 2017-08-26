from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['knowyourship.com', 'www.knowyourship.com']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {

    }
}


# Haystack and Solr

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr'
#        # ...or for multicore...
#        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
#    },
#}