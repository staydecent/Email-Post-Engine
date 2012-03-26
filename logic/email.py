import logging, datetime, email, yaml, re

import aws_s3 as s3

from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api import images as image

from models.entry import Entry, Category


class EntryHandler(InboundMailHandler):
    """
    Process inbound emails as entries into the database.

    Every email is a new post. User must login to web interface
    to edit any post details.

    message object:
     - subject
     - sender
     - to
     - cc
     - bodies
     - date
     - attachments

     optional fields within message.bodies:
      - slug (default message.subject)
      - published (default message.date)
      - draft
      - category
    """
    def receive(self, message):
        # Combine message bodies and decode html
        bodies = message.bodies('text/plain')

        for content_type, body in bodies:
            decoded_body = body.decode()

        # Split body from any optional fields
        body_list = decoded_body.split('---\n\n', 1)
        body_len  = len(body_list)
        fields = body_list[0]
        body = body_list[1]

        # grab the first paragraph as 
        body_parts = body.split('\n\n', 1)
        excerpt = body_parts[0]
        body = body_parts[1]

        # Grab any data from fields
        slug = message.subject.replace(' ', '-').lower()
        cat_name = "Bit"
        draft = False
        published = None

        if fields:
            logging.info("We have YAML front matter.")
            for config in yaml.load_all(fields):
                logging.info("Checking each YFM.")
                logging.debug(type(config))
                # hard-coded data extraction
                # Probably should do this a better way
                if 'slug' in config:
                    slug = config['slug']

                if 'published' in config:
                    published = config['published']

                if 'category' in config:
                    cat_name = config['category']

                if 'draft' in config:
                    draft = True
        else:
            logging.error("Malformed YFM: --------- " + fields)

        if published is None:
            date = message.date.split(' -');
            published = datetime.datetime.strptime(date[0], "%a, %d %b %Y %H:%M:%S")
        else:
            published = datetime.datetime.strptime(published, "%a, %d %b %Y %H:%M:%S")

        # get the category object
        category = db.Query(Category).filter("name =", cat_name).get()
        logging.info("Entry in cat: " + category.name + " from: " + cat_name)

        # Process attachments!!!!!!
        images = []
        thumbnail = None

        if cat_name == "Work":
            if message.attachments:
                # Check file extension of attachments
                re_filetype = re.compile("(.gif|.jpg|.jpeg|.png|.GIF|.JPG|.JPEG|.PNG)")
                    
                for att in message.attachments:
                    # att[0] = name, att[1] = payload
                    is_image = re_filetype.search(att[0])

                    filename, encoded_data = att 
                    data = encoded_data.payload 
                    if encoded_data.encoding: 
                        data = data.decode(encoded_data.encoding) 

                    if is_image:
                        # upload image
                        if thumbnail is None:
                            thumb = image.resize(data, 250)
                            thumbnail = s3.upload_image(filename, thumb, message.subject)
                        
                        new_image = s3.upload_image(filename, data, message.subject)
                        images.append(new_image)
                    else:
                        logging.info(att)
                        logging.info('Attachment was not an image.')

        # save
        # Okay, just hardcode email
        # author property is now string
        # check user.email() to author when in admin
        if message.sender == '':
            entry = Entry(
                author    = message.sender,
                title     = message.subject,
                slug      = slug,
                category  = category.key(),
                body      = body,
                excerpt   = excerpt,
                published = published,               
                draft     = draft,
                images    = images,
                thumbnail = thumbnail
            )
            entry.put()
            entry.index()


def main():
    application = webapp.WSGIApplication([
        EntryHandler.mapping()
    ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()