import os


def app_root(*path):
    root = os.path.dirname(os.path.abspath(__name__))
    if path:
        return os.path.join(root, *path)
    else:
        return root


def prefix_upload_folder(app):
    folder = app.config['UPLOAD_FOLDER']
    app.config['UPLOAD_FOLDER'] = app_root(folder)
