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


def get_directory_listing(dir: str) -> tuple[str, str]:
    """
    Given a directory, returns sorted lists of directories and files contained in that directory.
    """

    dirs: list = []
    files: list = []
    for path in dir.iterdir():
        if path.is_dir():
            dirs.append(str(path).split('/')[-1])
        else:
            files.append(str(path).split('/')[-1])
    return sorted(dirs), sorted(files)


def get_refresh() -> int:
    """
    Returns the user's preference for a refresh period in seconds, or None if no refresh is set.
    """

    return (
        (int(request.args['refresh']) if 'refresh' in request.args else None)
        if not app.config['DISABLE_REFRESH']
        else None
    )


def get_style() -> str:
    """
    Returns the user's preference for style, or the default style configured on the server.
    """

    return (
        request.args['style']
        if 'style' in request.args and request.args['style'] in app.config['ALL_STYLES']
        else app.config['STYLE']
    )


@bp.route('/', methods=['GET'])
def handle_root():
    """
    Redirect calls to the URL root ("/") to the configured root document, or else render the root directory listing.
    """

    if app.config['ROOT_DOCUMENT']:
        return redirect(app.config['ROOT_DOCUMENT'])
    else:
        return serve_path('/')


@bp.route('/<path:file_path>', methods=['GET'])
def serve_path(file_path):
    """
    Handle all other routes, handling the URL path as a file path relative to the app's DIRECTORY config option. Renders
    routes differently depending on what type of file they refer to.
    """

    path = Path(f'{app.config["DIRECTORY"]}/{file_path}').absolute()
    # Nonexistent files get a 404
    if not path.exists():
        return render_template('404.html.j2'), 404

    # Directories get a special page that lists the contents
    if path.is_dir():
        dirs, files = get_directory_listing(path)
        return render_template(
            'directory.html.j2',
            dirs=dirs,
            files=files,
            refresh_seconds=get_refresh(),
            style=get_style(),
        )

    # All other paths get served as files
    else:
        return serve_path_as_file(path)


def render_path(path):
    """
    Respond to requests for Markdown documents by rendering them to HTML.
    """

    if not path.exists() or not path.is_file():
        return render_template('404.html.j2'), 404
    with open(path, 'r') as fh:
        html = markdown(fh.read(), extensions=['md_in_html', 'tables'])
    return HTMLResponse(
        render_template(
            'markdown.j2',
            all_styles=app.config['ALL_STYLES'],
            default_style=app.config['STYLE'],
            html=html,
            refresh_seconds=get_refresh(),
            style=get_style(),
        )
    )


def serve_path_as_file(file_path):
    """
    Serve up the requested file. If it's a Markdown file, render it to HTML first.
    """

    # Reject the request if the path being requested is above the project's path to prevent data leaking
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
        return render_path(file_path)

    directory = Path('/'.join(file_path.parts[:-1])).resolve()
    file = file_path.parts[-1]
    return send_from_directory(directory, file)
