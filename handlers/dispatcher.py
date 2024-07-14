from .base import BaseHandler
from typing import Any

from handlers.controllers import (
    IndexController, 
    MatchesHistoryController, 
    NewMatchController, 
    MatchScoreController)

class Dispatcher(BaseHandler):
    def __init__(self) -> None:
        super().__init__()
        self.valid_routes = {
            "/": IndexController,
            "/new-match": NewMatchController,
            "/match-score": MatchScoreController,
            "/matches": MatchesHistoryController
        }

    def __call__(self, environ, start_response) -> Any:
        url = environ.get('PATH_INFO', '')
        controller_type = self.valid_routes.get(url, None)
        if controller_type is not None:
            controller = controller_type()
            return controller(environ, start_response)
        else:
            return self.send_error(environ, start_response, "404 Not Found")
