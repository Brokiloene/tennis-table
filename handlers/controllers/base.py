from urllib.parse import parse_qs

from ..base import BaseHandler

class BaseController(BaseHandler):    
    def __init__(self) -> None:
        super().__init__()
        self.response_headers = [
            ('Content-type', 'text/html')
            ]

    def __call__(self, environ, start_response):
        method = environ.get('REQUEST_METHOD', None)
        match method:
            case 'GET':
                return self.do_GET(environ, start_response)
            case 'POST':
                return self.do_POST(environ, start_response)
            case None:
                return self.send_error_page(environ, start_response, '400 Bad Request')
    
    def do_GET(self, environ, start_response):
        pass

    def do_POST(self, environ, start_response):
        pass
        
    def parse_post_form(self, environ):
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        return parse_qs(request_body.decode('utf-8'))
    
    def get_query_param(self, environ, param: str) -> str:
        query = environ['QUERY_STRING']
        res = parse_qs(query)[param][0]
        return res
    
    def send_page(self, html_page, start_response):
        status = "200 OK"
        self.response_headers.append(
            ('Content-Length', str(len(html_page)))
        )
        start_response(status, self.response_headers)
        return [bytes(html_page, 'utf-8')]


    def redirect_to(self, location: str, start_response):
        status = '303 See other'
        self.response_headers.append(('Location', location))
        html_page = 'Redirecting...'
        self.response_headers.append(
            ('Content-Length', str(len(html_page)))
        )
        start_response(status, self.response_headers)
        return [bytes(html_page, 'utf-8')]

    def __iter__(self):
        pass
    