import os

from flask import Flask
from flask._compat import string_types

from narcissus.exts import setup_database
from narcissus.master.view import master_app
from narcissus.album.view import album_app
from narcissus.slider.view import slider_app


def app_root(*path):
    root = os.path.dirname(os.path.abspath(__name__))
    if path:
        return os.path.join(root, *path)
    else:
        return root


def prefix_upload_folder(app):
    folder = app.config['UPLOAD_FOLDER']
    app.config['UPLOAD_FOLDER'] = app_root(folder)


def create_app(import_name=None, config=None):
    app = Flask(import_name or __name__)

    app.config.from_object('narcissus.settings')

    if isinstance(config, dict):
        app.config.update(config)
    elif isinstance(config, string_types):
        app.config.from_pyfile(os.path.abspath(config))

    prefix_upload_folder(app)

    setup_database(app)

    app.register_blueprint(master_app)
    app.register_blueprint(album_app)
    app.register_blueprint(slider_app)

    return app
