import os

from flask.ext.script import Manager, Server

from narcissus.app import create_app


app_root = os.path.dirname(os.path.abspath(__name__))

application = create_app('narcissus', os.path.join(app_root, 'development.conf'))
server = Server()
manager = Manager(application)
manager.add_command('runserver', server)


@manager.option('-p', dest='port', help='port of host', default=5000)
def run(port):
    """Run app at 0.0.0.0"""
    application.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    manager.run()
