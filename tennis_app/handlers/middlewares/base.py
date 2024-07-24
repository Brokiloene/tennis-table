from typing import Any

from ..base import BaseHandler

class BaseMiddleware(BaseHandler):
    def __init__(self, application) -> None:
        super().__init__()
        self.app = application
    
    def __call__(self, environ, start_response) -> Any:
        pass

