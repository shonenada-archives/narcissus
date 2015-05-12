from flask import Blueprint, render_template, request, current_app, jsonify
from flask import redirect, url_for

from narcissus.exts import db
from narcissus.settings import UPLOAD_THUMBNAIL
from narcissus.master.model import Tag
from narcissus.album.model import Image
from narcissus.album.service import save_image
from narcissus.thumb.service import thumbnail_img


master_app = Blueprint('master', __name__)


@master_app.route('/')
def index():
    return render_template('index.html')


@master_app.route('/upload', methods=['POST',])
def upload():
    image = request.files['image']
    data = image.stream.read()
    path = save_image(data)

    img = Image(path=path)
    db.session.add(img)
    db.session.commit()

    if UPLOAD_THUMBNAIL:
        thumbnail_img(data, img)

    return jsonify(success=True)


@master_app.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@master_app.route('/tags/create', methods=['GET', 'POST'])
def tag_create():
    if request.method == 'GET':
        return render_template('tag_create.html')
    elif request.method == 'POST':
        name = request.form['name']
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('master.tags'))
