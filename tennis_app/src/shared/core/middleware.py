from typing import Any
from abc import ABC, abstractmethod

from .handler import BaseHandler

class BaseMiddleware(ABC, BaseHandler):
    def __init__(self, application) -> None:
        super().__init__()
        self.app = application
    
    @abstractmethod
    def __call__(self, environ, start_response) -> Any:
        pass

