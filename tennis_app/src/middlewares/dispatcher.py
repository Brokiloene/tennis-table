from typing import Any

# from tennis_app.src.shared.core import BaseHandler
from tennis_app.src.shared.core import BaseMiddleware
from tennis_app.src.modules import (
    IndexController, 
    MatchesHistoryController, 
    NewMatchController, 
    MatchScoreController
)
from tennis_app.src.views import ResponseMsg

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
            return self.send_response(
                start_response,
                self.view.msg.NOT_FOUND,
                ['text/html'],
                self.view,
                ["error-page", {"error_message": self.view.msg.NOT_FOUND}]
            )
        else:
            controller(environ, start_response, self.view)
        controller_type = self.routes.get(url, None)
        if controller_type is not None:
            controller = controller_type()
            return controller(environ, start_response, self.view)
        else:
            return self.send_response(
                start_response,

            )
            return self.send_error_response(
                environ, 
                start_response, 
                ResponseMsg.NOT_FOUND, 
                self.view
            )
