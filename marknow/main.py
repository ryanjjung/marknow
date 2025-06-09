#!/bin/env python3

"""
A Flask server that renders Markdown files and provides a method for navigating these documents in a web browser.
"""

import logging
import os

from argparse import ArgumentParser, Namespace
from flask import Flask
from marknow.lib import monitor, renderer
from pathlib import Path


def __get_styles() -> list[str]:
    """
    Returns a list of available stylesheets.
    """

    styles_path: Path = Path.cwd() / 'marknow' / 'static' / 'styles'
    return [
        ''.join(file.split('.')[:-1]) for file in [path.name for path in styles_path.glob('*.css') if path.is_file()]
    ]


def parse_args() -> Namespace:
    """
    Support the use of these command line arguments
    """

    parser = ArgumentParser(description='Serve browsable Markdown')
    parser.add_argument('directory', help='Path to the top level of Markdown files to serve')
    parser.add_argument('-a', '--address', help='Bind address', default='127.0.0.1')
    parser.add_argument(
        '-d',
        '--disable-refresh',
        help="Disable clients's ability to auto-refresh pages",
        default=False,
        action='store_true',
    )
    parser.add_argument('-p', '--port', help='Port to listen on', default=4037)
    parser.add_argument('-r', '--root', help='File to redirect calls to "/" to', default=None)
    parser.add_argument(
        '-s',
        '--style',
        help='Filename in `static/styles` directory to render',
        choices=__get_styles(),
        default='default',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='Enable verbose logging',
        default=False,
        action='store_true',
    )
    return parser.parse_args()


def setup_logging(verbose: bool = False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


def create_app(directory: str, root: str, style: str, verbose: bool, disable_refresh: bool) -> Flask:
    """
    Create the Marknow Flask application with various options set.
    """

    setup_logging(verbose=verbose)
    blueprints = [monitor.bp, renderer.bp]
    template_dir = Path.cwd() / 'marknow/templates'
    static_folder = Path.cwd() / 'marknow/static'
    app = Flask(__name__, template_folder=template_dir, static_folder=static_folder)
    app.logger.debug('New app created')
    app.config['DIRECTORY'] = os.environ.get('MN_MARKDOWN_DIRECTORY', directory)
    app.config['DISABLE_REFRESH'] = disable_refresh
    app.config['ROOT_DOCUMENT'] = os.environ.get('MN_ROOT_DOCUMENT', root)
    app.config['STYLE'] = os.environ.get('MN_STYLE', style)
    app.logger.debug('App configured')
    for bp in blueprints:
        app.register_blueprint(bp)
        app.logger.debug(f'Registered blueprint: {bp}')
    return app


def main():
    """
    Parse command line options and pass some of them into the Flask app.
    """

    args = parse_args()
    app = create_app(args.directory, args.root, args.style, args.verbose, args.disable_refresh)
    app.run(host=args.address, port=args.port, debug=args.verbose)


if __name__ == '__main__':
    main()
