from StringIO import StringIO

import Image
from werkzeug import secure_filename
from flask import current_app, make_response

from narcissus.settings import UPLOAD_STRATEGY
from narcissus.album.model import Image as ImageModel, ImageData


class UnknownStrategyError(Exception):
    pass


def compress_raw_img(raw_data):
    img = Image.open(StringIO(raw_data))
    stream = StringIO()
    img.save(stream, 'JPEG' if img.format != 'GIF' else 'GIF', quality=100)
    data = stream.getvalue()
    stream.close()
    return data


def save_image(data):
    if UPLOAD_STRATEGY == 'blob':
        ret = save_image_blob(data)
        return 'path://%s:%s' % ret
    elif UPLOAD_STRATEGY == 'file':
        return save_image_file(data)
    raise UnknownStrategyError()


def save_image_blob(data):
    if current_app.config.get('UPLOAD_COMPRESS', False):
        data = compress_raw_img(data)

    image = ImageData(data)
    image_id = image.save()
    db_id = image.db_id
    return (db_id, image_id)


def save_image_file(data):
    pass


def parse_path(path):
    db_id, image_id = path[7:].split(':', 1)
    return db_id, image_id


def image_response(img):
    filename = img.title or 'img'
    disposition = 'attachment; filename=%s.jpg' % filename
    if not img.path[:4] is 'path':
        return abort(404)

    db_id, image_id = parse_path(img.path)
    img_data = ImageQuery.get(db_id, image_id)
    if not img_data:
        return abort(404)

    response = make_response(str(img_data['data']))
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Content-Disposition'] = disposition
    return response
