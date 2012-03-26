import os
import datetime
import logging
import markdown

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

from models.entry import Entry
from root import template_dir

 
class FeedHandler(webapp.RequestHandler):

    def get_entries(self):
        mem_key = "FeedEntries"

        entries = memcache.get(mem_key)
        if entries is not None:
            return entries
        else:
            entries = db.Query(Entry).filter('draft = ', False).order('-published').fetch(limit=25)
            for i in range(len(entries)):
                entries[i].body = markdown.markdown(entries[i].body)
                """ Output datetime in RFC 3339 format that is also valid ISO 8601
                    timestamp representation"""
                updated = entries[i].updated
                if updated.tzinfo is None:
                    suffix = "-00:00"
                else:
                    suffix = updated.strftime("%z")
                    suffix = suffix[:-2] + ":" + suffix[-2:]
                entries[i].atom_updated = entries[i].updated.strftime("%Y-%m-%dT%H:%M:%S") + suffix
                
                published = entries[i].published
                if published.tzinfo is None:
                    suffix = "-00:00"
                else:
                    suffix = published.strftime("%z")
                    suffix = suffix[:-2] + ":" + suffix[-2:]
                entries[i].atom_published = entries[i].published.strftime("%Y-%m-%dT%H:%M:%S") + suffix

            memcache.add(mem_key, entries, 86400) # day
            return entries
    
    def get(self):
        entries = self.get_entries()

        nowdate = datetime.datetime.now()
        if nowdate.tzinfo is None:
            suffix = "-00:00"
        else:
            suffix = nowdate.strftime("%z")
            suffix = suffix[:-2] + ":" + suffix[-2:]
        atom_now = nowdate.strftime("%Y-%m-%dT%H:%M:%S") + suffix
            
        self.response.headers["Content-Type"] = "application/atom+xml"
        path = os.path.join(template_dir, 'feed', 'posts.xml')
        data = {'entries': entries, 'atom_now': atom_now}
        self.response.out.write(template.render(path, data))


def main():
    application = webapp.WSGIApplication([
        ("/feed/?", FeedHandler)
    ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()