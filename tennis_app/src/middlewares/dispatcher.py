from typing import Any

# from tennis_app.src.shared.core import BaseHandler
from tennis_app.src.shared.core import BaseMiddleware, BaseController
from tennis_app.src.shared.http_status import HttpStatus
from tennis_app.src.modules import (
    IndexController,
    MatchesHistoryController,
    NewMatchController,
    MatchScoreController,
)


class Dispatcher(BaseMiddleware):
    def __init__(self) -> None:
        self.routes = {
            "/": IndexController(),
            "/new-match": NewMatchController(),
            "/match-score": MatchScoreController(),
            "/matches": MatchesHistoryController(),
        }
        print(self.routes)

    def __call__(self, environ, start_response) -> Any:
        url: str = environ.get("PATH_INFO", "")
        controller: BaseController | None = self.routes.get(url, None)
        print(controller)
        if controller is None:
            return self.send_error(
                start_response, HttpStatus.NOT_FOUND, BaseController.headers
            )
        else:
            return controller(environ, start_response)
