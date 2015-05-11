import os

from flask.ext.script import Manager, Server

from narcissus.app import create_app
from narcissus.exts import db


app_root = os.path.dirname(os.path.abspath(__name__))

application = create_app('narcissus', os.path.join(app_root, 'development.conf'))
server = Server()
manager = Manager(application)
manager.add_command('runserver', server)


@manager.option('-c', dest='config', help='Config file',
                default='development.conf')
@manager.option('-d', dest='destroy', help='Destroy database', default=False)
def create_db(config, destroy):
    config_file = os.path.join(app_root, config)
    application.config.from_pyfile(config_file)
    with application.test_request_context():
        if destroy:
            db.drop_all()
        from narcissus.master.model import Tag
        from narcissus.album.model import Album, Image, Thumb
        db.create_all()
    print 'Created Database!'


@manager.option('-p', dest='port', help='port of host', default=5000)
def run(port):
    """Run app at 0.0.0.0"""
    application.run(host='0.0.0.0', port=port, debug=True)


@manager.option('-c', dest='config', help='Config file',
                default='development.conf')
@manager.option('-d', dest='destroy', help='Destroy database', default=True)
def syncdb(config, destroy):
    create_db(config, destroy)


if __name__ == '__main__':
    manager.run()
