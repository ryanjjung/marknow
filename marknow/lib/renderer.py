"""Handle routes related to rendering Markdown or listing files in the
document root.
"""

from flask import (
    Blueprint,
    current_app as app,
    redirect,
    request,
    render_template,
    send_from_directory,
)
from marknow.lib import HTMLResponse
from markdown import markdown
from pathlib import Path

bp = Blueprint('renderer', __name__)


def get_directory_listing(dir):
    """Given a directory, returns a sorted list of directories and files
    contained in that directory
    """

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
    """Redirect calls to the URL root ("/") to the configured root document."""
    if app.config['ROOT_DOCUMENT']:
        return redirect(app.config['ROOT_DOCUMENT'])
    else:
        return serve_path('/')


@bp.route('/<path:file_path>', methods=['GET'])
def serve_path(file_path):
    """Handle routes that indicate directories (not renderable files)"""

    path = Path(f'{app.config["DIRECTORY"]}/{file_path}').absolute()
    if not path.exists():
        return render_template('404.html.j2'), 404
    if path.is_dir():
        dirs, files = get_directory_listing(path)
        return render_template('directory.html.j2', dirs=dirs, files=files, style=app.config['STYLE'])
    else:
        refresh_seconds = request.args['refresh'] if 'refresh' in request.args else None
        return serve_path_as_file(path, refresh_seconds)


def render_path(path, refresh_seconds=None):
    """Handle routes that indicate Markdown files in need of rendering"""

    if not path.exists() or not path.is_file():
        return render_template('404.html.j2'), 404
    with open(path, 'r') as fh:
        html = markdown(fh.read(), extensions=['md_in_html', 'tables'])
    return HTMLResponse(
        render_template(
            'markdown.j2',
            html=html,
            refresh_seconds=refresh_seconds,
            style=app.config['STYLE'],
        )
    )


def serve_path_as_file(file_path, refresh_seconds=None):
    """Handle all other routes, treating them as files to deliver directly"""

    # Reject the request if the path being requested is above the project's path
    highest_path = Path(f'{app.config["DIRECTORY"]}').absolute()
    try:
        file_path.relative_to(highest_path)
    except ValueError:
        return render_template('400.html.j2'), 400

    # 404 if the file doesn't exist
    if not file_path.exists() or not file_path.is_file():
        return render_template('404.html.j2'), 404

    # Render Markdown files
    if file_path.parts[-1][-3:] == '.md':
        return render_path(file_path, refresh_seconds)

    directory = Path('/'.join(file_path.parts[:-1])).resolve()
    file = file_path.parts[-1]
    return send_from_directory(directory, file)
