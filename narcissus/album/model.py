import os
import shutil
import sqlite3

from flask import url_for, current_app

from narcissus.app import app_root
from narcissus.settings import IMG_DB_THRESHOLD
from narcissus.exts import db
from narcissus.master.model import tags


DB_TEMPLATE_PATH = app_root('narcissus/misc/template.db')


class UnknownPathError(Exception):
    pass


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('images'))
    path = db.Column(db.String(500))

    @property
    def link(self):
        if self.path[:4] == 'http':
            return self.path
        elif self.path[:4] == 'path':
            return url_for('album.blob', id=self.id)
        raise UnknownPathError('path %s cannot be recognited')


class ImageData(object):

    def __init__(self, data):
        self.data = data
        self._db_id = None
        self.image_id = None
        self.conn = None

    @property
    def db_id(self):
        if not self._db_id:
            count = Image.query.count()
            self._db_id = count / IMG_DB_THRESHOLD
        return self._db_id

    def connect(self):
        slice_path = current_app.config['IMG_SLICE_PATH']
        data_path = slice_path % self.db_id
        if not os.path.exists(data_path):
            shutil.copy(DB_TEMPLATE_PATH, data_path)
        self.conn = sqlite3.connect(data_path)

    def cloes(self):
        self.conn.close()

    def save(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO images(data) VALUES(?)',
                       [buffer(self.data)])
        self.conn.commit()
        self.image_id = cursor.lastrowid
        return self.image_id


class ImageQuery(object):

    @classmethod
    def connect(self, db_id):
        conn = sqlite3.connect(current_app.config['IMG_SLICE_PATH'] % db_id)
        return conn

    @classmethod
    def get(self, db_id, image_id):
        conn = ImageQuery.connect(db_id)
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM images WHERE id = ?', [image_id])
        row = cursor.fetchone()
        if not row:
            return None
        ret = {
            'id': image_id,
            'data': row[0]
        }
        conn.close()
        return ret
