from flask import Blueprint, abort, url_for, render_template, request
from flask import redirect

from narcissus.exts import db
from narcissus.album.model import Album, Image, ImageQuery
from narcissus.album.service import parse_path


album_app = Blueprint('album', __name__)


@album_app.route('/album')
def album_index():
    return "Hello"


@album_app.route('/album/blob/<int:id>')
def album_blob(id):
    img = Image.query.get_or_404(id)
    return image_response(img)


@album_app.route('/album/image/<int:id>')
def album_image(id):
    img = Image.query.get_or_404(id)
    return '''<img src="%s" />''' % (url_for('album.album_blob', id=id))


@album_app.route('/album/list')
def album_list():
    albums = Album.query.all()
    return render_template('albums.html', albums=albums)


@album_app.route('/album/create', methods=['GET', 'POST'])
def album_create():
    if request.method == 'GET':
        return render_template('album_create.html')
    else:
        name = request.form.get('name')
        album = Album(name=name)
        db.session.add(album)
        db.session.commit()
        return redirect(url_for('album.album_list'))
