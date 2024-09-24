from tennis_app.src.shared.core import BaseController
from .ui.view import MainPageView

class IndexController(BaseController):
    def do_GET(self, environ, start_response):
        data = MainPageView({})
        return self.send_response(start_response, self.headers, data)
