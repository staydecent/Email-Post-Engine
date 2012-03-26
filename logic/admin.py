import os
import cgi
import datetime
import search

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api import urlfetch
from django.utils import simplejson as json
from models.entry import Entry
from root import template_dir

class NewEntryHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join( template_dir, 'admin', 'new.html' )
        self.response.out.write( template.render(path, {}) )

    def post(self):
        entry = Entry(
            author   = users.get_current_user().email(),
            title    = self.request.get('title'),
            slug     = self.request.get("slug"),
            # tags     = self.request.get("tags"),
            template = self.request.get("template"),
            body     = self.request.get("body"),
            draft    = bool(self.request.get("draft"))
        )
        entry.put()
        entry.index()
        self.redirect("/" + entry.category.slug + "/" + entry.slug)
      
        
class EditEntryHandler(webapp.RequestHandler):
    def get(self, slug):
        entry = db.Query(Entry).filter("slug =", slug).get()
        if not entry:
            path = os.path.join(template_dir, 'admin', '404.html')
            self.response.out.write(template.render(path, {'err': '404'}))
        else:          
            path = os.path.join( template_dir, 'admin', 'edit.html' )
            self.response.out.write( template.render(path, { 'entry':entry }) )

    def post(self, slug):
        key = self.request.get("key", None)
        entry = Entry.get(key)
        
        entry.title     = self.request.get('title')
        entry.slug      = self.request.get("slug")
        # entry.published = datetime.datetime.strptime( self.request.get("published"), "%Y-%m-%d %H:%M:%S" )
        entry.excerpt   = self.request.get("excerpt")
        entry.body      = self.request.get("body")
        entry.draft     = bool(self.request.get("draft"))
        
        entry.put()
        entry.index()
        entry.indexed_title_changed()
        self.redirect("/entry/" + entry.slug)


def main():
    application = webapp.WSGIApplication([
        ("/admin/new/?", NewEntryHandler),
        ("/admin/edit/([^/]+)/?", EditEntryHandler),
        ("/tasks/searchindexing", search.SearchIndexing)
    ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()