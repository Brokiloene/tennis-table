from tennis_app.src.shared.core import BaseController
from .view import MainPageView


class IndexController(BaseController):
    def do_GET(self, environ, start_response):
        data: str = MainPageView.render({})
        return self.send_response(start_response, self.headers, data)
