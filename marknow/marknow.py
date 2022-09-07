#!/bin/env python3

from argparse import ArgumentParser
from flask import Flask
from lib import monitor

def parse_args():
    parser = ArgumentParser(description='Serve browsable Markdown')
    parser.add_argument('directory',
        help='Path to the top level of Markdown files to serve')
    parser.add_argument('-a', '--address',
        help='Bind address',
        default='127.0.0.1')
    parser.add_argument('-p', '--port',
        help='Port to listen on',
        default=4037)
    parser.add_argument('-v', '--verbose',
        help='Enable verbose logging',
        default=False,
        action='store_true')
    return parser.parse_args()

def create_app():
    '''Create the Marknow Flask application
    '''

    blueprints = [
        monitor.bp
    ]
    app = Flask(__name__)
    app.logger.debug('New app created')
    for bp in blueprints:
        app.register_blueprint(bp)
        app.logger.debug(f'Registered blueprint: {bp}')
    return app

def main():
    args = parse_args()
    app = create_app()
    app.run(host=args.address, port=args.port, debug=args.verbose)

if __name__ == '__main__':
    main()
