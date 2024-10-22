import mimetypes
from pathlib import Path
from datetime import datetime

from tennis_app.src.shared.core import BaseMiddleware
from tennis_app.src.shared.http_status import HttpStatus


class StaticFileMiddleware(BaseMiddleware):
    def __init__(self, application, static_dir) -> None:
        super().__init__(application)
        self.app = application
        self.static_dir = Path(static_dir)

    def get_content_type(self, path: Path) -> str:
        # guess_type() returns tuple (type, encoding)
        return mimetypes.guess_type(path)[0]
    
    def find_static_file(self, path: Path) -> Path:
        # search for static file. Result must be unique
        found_files = list(self.static_dir.glob(f"*/{path}"))
        if len(found_files) == 1:
            return found_files[0]
        else:
            return Path()
    
    def send_file(self, environ, start_response, file_path, mime_type):
        mod_time = datetime.fromtimestamp(
            file_path
            .stat()
            .st_mtime).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        file_size = file_path.stat().st_size
        response_headers = [
            ('Content-Type', mime_type),
            ('Content-Length', str(file_size)),
            ('Last-modified', mod_time)
        ]
        start_response('200 OK', response_headers)
        f = open(file_path, 'rb')
        return environ['wsgi.file_wrapper'](f, file_size)

    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').lstrip('/')
        file_path = self.find_static_file(path)
        mime_type = self.get_content_type(path)

        if not file_path.is_file():
            return self.app(environ, start_response)
        elif mime_type is None:
            # CHANGE
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)
        else:
            return self.send_file(environ, start_response, file_path, mime_type)
