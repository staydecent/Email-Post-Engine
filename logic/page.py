import os, re, markdown

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from models.entry import Entry, Category
from root import template_dir  


class IndexHandler(webapp.RequestHandler):
    """
    Display the latest blog posts.
    """
    def get(self):
        cat_article = db.Query(Category).filter('name =', 'Article').get()
        cat_bit = db.Query(Category).filter('name =', 'Bit').get()
        cat_work = db.Query(Category).filter('name =', 'Work').get()

        articles = db.Query(Entry).filter('draft = ', False).order('-published')
        articles = articles.filter('category =', cat_article.key()).fetch(limit=3)

        bits = db.Query(Entry).filter('draft = ', False).order('-published')
        bits = bits.filter('category =', cat_bit.key()).fetch(limit=10)

        work = db.Query(Entry).filter('draft = ', False).order('-published')
        work = work.filter('category =', cat_work.key()).fetch(limit=5)

        path = os.path.join(template_dir, 'home.html')
        data = {
            'articles': articles, 
            'bits': bits,
            'work':work
        }
        self.response.out.write(template.render(path, data))


class EntryHandler(webapp.RequestHandler):
    """
    Baiscally the single page for a blogpost.
    """
    def get(self, cat, slug):
        entry = db.Query(Entry).filter("slug =", slug).get()
        if not entry:
            path = os.path.join(template_dir, '404.html')
            self.response.out.write(template.render(path, {'err': '404'}))
        else:
            next = db.Query(Entry).filter('category =', entry.category).order('-published').filter("published <", entry.published).get()
                 
            body = markdown.markdown(entry.body)
            entry.body = body

            data = {
                'e':entry,
                'next':next,
                'sitetitle':entry.title+' &middot; Staydecent',
                'description':entry.excerpt
            }

            if cat == "work":
                path = os.path.join(template_dir, 'entry.work.html')
            else:
                path = os.path.join(template_dir, 'entry.html')

            self.response.out.write(template.render(path, data))


class CategoryHandler(webapp.RequestHandler):
    """
    Display the archive of all posts.
    """
    def get(self, slug):
        category = db.Query(Category).filter('slug =', slug).get()
        entries = db.Query(Entry).filter('draft =', False).filter('category =', category.key()).order('-published').fetch(limit=99)

        for i in range(len(entries)):
            body = markdown.markdown(entries[i].body)
            entries[i].body = body
        
        if slug == "work":
            path = os.path.join(template_dir, 'archive.work.html')  
        else:  
            path = os.path.join(template_dir, 'archive.html')

        data = {
            'entries': entries,
            'category':category,
            'current':category.slug,
            'sitetitle': category.name + 's &middot; Staydecent'
        }
        self.response.out.write(template.render(path, data))


class PageHandler(webapp.RequestHandler):
    """
    Pages
    """
    def get(self, slug):
        path = os.path.join(template_dir, slug + '.html')
        data = {
            'sitetitle': slug.title() + ' &middot; Staydecent'
        }
        self.response.out.write(template.render(path, data))


class RedirectHandler(webapp.RequestHandler):
    """
    Redirect old /entry/ urls
    """
    def get(self, slug):
        entry = db.Query(Entry).filter("slug =", slug).get()
        if not entry:
            path = os.path.join(template_dir, '404.html')
            self.response.out.write(template.render(path, {'err': '404'}))
        else:
            new_url = '/' + entry.category.slug + '/' + slug
            self.redirect(new_url, permanent=True)


class PaginationHandler(webapp.RequestHandler):
    """
    Display the latest blog posts with pagination.

    Same function as BlogHandler but offsets the results based on 'number'.
    """
    def get(self, number):
        offset = 10*(int(number)-1)
        entries_count = Entry.all(keys_only=True).count()
        if entries_count / 10 >= number:
            number = number+1
        else:
            number = False

        entries = db.Query(Entry).filter('draft = ', False).order('-published').fetch(limit=10, offset=offset)
        for i in range(len(entries)):
            body = markdown.markdown(entries[i].body)
            entries[i].body = body
            
        path = os.path.join(template_dir, 'blog.html')
        data = {'entries': entries, 'sitetitle': 'The Staydecent&trade; Web Design &amp; Development Blog', 'number':number}
        self.response.out.write(template.render(path, data))


class SearchHandler(webapp.RequestHandler):
    """
    Search results!
    """
    def get(self):
        phrase = self.request.get('phrase')
        results = Entry.search(phrase)
        path = os.path.join(template_dir, 'search.html')
        data = {'results': results, 'phrase': phrase, 'sitetitle': 'Results for &ldquo;'+phrase+'&rdquo; &middot; Staydecent'}
        self.response.out.write(template.render(path, data))


class ErrorHandler(webapp.RequestHandler):

    def get(self):
        path = os.path.join(template_dir, '404.html')
        self.response.out.write(template.render(path, {
            'err': '404', 
            'sitetitle': '404, Not found: The Staydecent&trade; Web Design &amp; Development Blog'
        }))


# serve that shit 
urls = [
    ("/?", IndexHandler),
    ("/(articles|bits|work)/?", CategoryHandler),
    ("/(articles|bits|work)/([^/]+)/?", EntryHandler),
    ("/(about|contact)/?", PageHandler),
    ('/search/?', SearchHandler),
    ('/entry/([^/]+)/?', RedirectHandler),
    ("/.*", ErrorHandler)
]

def main():
    application = webapp.WSGIApplication(urls, debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()