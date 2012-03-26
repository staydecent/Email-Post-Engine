import os, search

from google.appengine.ext import db


class Category(db.Model):

    name = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)


class Entry(search.Searchable, db.Expando):
    
    author      = db.StringProperty(required=False)
    title       = db.StringProperty(required=True)
    slug        = db.StringProperty(required=True)
    category    = db.ReferenceProperty(Category)
    body        = db.TextProperty(required=True)
    excerpt     = db.TextProperty(required=False)
    published   = db.DateTimeProperty(auto_now_add=True)
    updated     = db.DateTimeProperty(auto_now=True)
    draft       = db.BooleanProperty(default=False)
    images      = db.StringListProperty()
    thumbnail   = db.StringProperty()

    INDEX_ONLY  = ['title', 'body']
    INDEX_TITLE_FROM_PROP = 'title'

    def permalink(self):
        return self.category.slug + '/' + self.slug