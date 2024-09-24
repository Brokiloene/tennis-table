from urllib.parse import parse_qs

from .handler import BaseHandler

class BaseController(BaseHandler):    
    def __init__(self) -> None:
        self.response_headers = [
            ('Content-type', 'text/html')
            ]

    def __call__(self, environ, start_response, view):
        method = environ.get('REQUEST_METHOD', None)
        match method:
            case 'GET':
                return self.do_GET(environ, start_response)
            case 'POST':
                return self.do_POST(environ, start_response)
            case None:
                return self.send_response(
                    start_response, 
                    self.status.BAD_REQUEST,
                    self.response_headers,
                    view,
                    {"error_message": self.status.BAD_REQUEST}
                )
                # return self.send_error_response(environ, start_response, '400 Bad Request', view)
    
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


    def redirect_to(self, location: str, start_response):
        status = '303 See other'
        self.response_headers.append(('Location', location))
        res = 'Redirecting...'
        self.response_headers.append(
            ('Content-Length', str(len(res)))
        )
        start_response(status, self.response_headers)
        return [bytes(res, 'utf-8')]

    def __iter__(self):
        pass
    