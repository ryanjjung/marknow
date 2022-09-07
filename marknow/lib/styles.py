from flask import Blueprint
from pathlib import Path

bp = Blueprint('styles', __name__)

@bp.route('/_styles/<path:style_path>')
def serve_style_file(style_path):
    path = Path('')
