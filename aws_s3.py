import boto

# Gotta fill these out!

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

AWS_BUCKET_NAME = ''


def get_bucket():
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(AWS_BUCKET_NAME)
    return bucket

def upload_image(filename, data, entry_title):
    import uuid
    from boto.s3.key import Key

    bucket = get_bucket()
    new_image = Key(bucket)
    image_uuid = str(uuid.uuid4())

    new_image.key = image_uuid
    new_image.set_metadata('filename', filename)
    new_image.set_metadata('entry_title', entry_title)
    new_image.set_metadata('Content-Type', 'image/png')
    new_image.set_contents_from_string(data, policy='public-read')

    return image_uuid