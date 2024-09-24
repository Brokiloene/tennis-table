from tennis_app.src.shared.core import BaseController
from tennis_app.src.views import htmlView


class IndexController(BaseController):
    def do_GET(self, environ, start_response):
        res = htmlView("index", dict())
        return self.send_response(res, start_response)
