from flask import Blueprint
from lib import HTMLResponse

HTML = """<!DOCTYPE html>
<html>
<head><title>I'm Alive!</title></head>
<body><h1>I'm Alive!</h1></body>
</html>
"""

bp = Blueprint("monitor", __name__, url_prefix="/_")


@bp.route("/ping", methods=["GET"])
def ping():
    """Return a successful message to show the service is alive. To be used
    as a health check.
    """
    return HTMLResponse(status=200, response=HTML)
