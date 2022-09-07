from flask import Blueprint, current_app as app, redirect, render_template
from lib import HTMLResponse
from markdown import markdown
from pathlib import Path

bp = Blueprint('renderer', __name__)

def get_directory_listing(dir):
    dirs = []
    files = []
    for path in dir.iterdir():
        if path.is_dir():
            dirs.append(str(path).split('/')[-1])
        else:
            files.append(str(path).split('/')[-1])
    return sorted(dirs), sorted(files)

@bp.route('/', methods=['GET'])
def redirect_root():
    return redirect(app.config['ROOT_DOCUMENT'])

@bp.route('/<path:dir_path>/', methods=['GET'])
def servce_dir(dir_path):
    path = Path(f"{app.config['DIRECTORY']}/{dir_path}")
    if not path.exists() or not path.is_dir():
        return render_template('404.html.j2'), 404
    dirs, files = get_directory_listing(path)
    return render_template('directory.html.j2', dirs=dirs, files=files)

@bp.route('/<path:file_path>.md', methods=['GET'])
def serve_path(file_path):
    path = Path(f"{app.config['DIRECTORY']}/{file_path}.md")
    if not path.exists() or not path.is_file():
        return render_template('404.html.j2'), 404
    with open(path, 'r') as fh:
        html = markdown(fh.read())
    return HTMLResponse(render_template('markdown.j2', html=html))
