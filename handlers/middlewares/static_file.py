import mimetypes
from pathlib import Path

from typing import List

from .base import BaseMiddleware


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
    
    def get_file_data(self, path: Path) -> List[bytes]:
         with open(path, 'rb') as file:
            return [file.read()]

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '').lstrip('/')
        file_path = self.find_static_file(path)
        mime_type = self.get_content_type(path)
        if not file_path.is_file():
            return self.app(environ, start_response)
        elif mime_type is None:
            return self.send_error(environ, start_response, "400 Bad Request")
        else:
            data = self.get_file_data(file_path)
            response_headers = [
                ('Content-Type', mime_type),
                ('Content-Length', str(file_path.stat().st_size))
            ]
            start_response('200 OK', response_headers)
            return data  
        