import os

from google.appengine.api import urlfetch
from google.appengine.api import memcache
from django.utils import simplejson as json

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

# pass album id as key, query picasa api or memcache
def get_photos(key):
    photos = memcache.get("photos:%s" % key)
    if not photos:
        url = 'http://picasaweb.google.com/data/feed/api/user/unger.adrian/albumid/'+key+'?alt=json'
        photos = json.loads( urlfetch.fetch(url).content )
        memcache.set("photos:%s" % key, photos)
    return photos
		