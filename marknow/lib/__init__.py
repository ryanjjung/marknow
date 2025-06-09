from flask import Response


class HTMLResponse(Response):
    """
    Simple Response override that indicates HTML in the body.
    """

    def __init__(self, *args, **kwargs):
        kwargs['content_type'] = 'text/html'
        super().__init__(*args, **kwargs)
