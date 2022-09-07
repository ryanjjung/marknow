from flask import Response

class HTMLResponse(Response):
    def __init__(self, *args, **kwargs):
        kwargs['content_type'] = 'text/html'
        super().__init__(*args, **kwargs)
