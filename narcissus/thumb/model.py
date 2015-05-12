from narcissus.exts import db


class Thumb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('image.id'))
    path = db.Column(db.String(500))

    @property
    def mode(self):
        return path[:4]


class ThumbData(db.Model):

    __bind_key__ = 'thumb_db'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Binary)
