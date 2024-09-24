from typing import Any

# from tennis_app.src.shared.core import BaseHandler
from tennis_app.src.shared.core import BaseMiddleware
from tennis_app.src.shared.http_status import HttpStatus
from tennis_app.src.modules import (
    IndexController, 
    MatchesHistoryController, 
    NewMatchController, 
    MatchScoreController
)

class Dispatcher(BaseMiddleware):
    def __init__(self, view) -> None:
        self.view = view
        self.routes = {
            "/": IndexController(),
            "/new-match": NewMatchController(),
            "/match-score": MatchScoreController(),
            "/matches": MatchesHistoryController()
        }

    def __call__(self, environ, start_response) -> Any:
        url = environ.get('PATH_INFO', '')
        controller = self.routes.get(url, None)
        if controller is None:
            return self.send_error(start_response, HttpStatus.NOT_FOUND, self.headers)
        else:
            controller(environ, start_response, self.view)
