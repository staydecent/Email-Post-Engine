import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'

from google.appengine.dist import use_library
use_library('django', '1.2')