from .base import BaseController

class IndexController(BaseController):

    def do_GET(self, environ, start_response):
        html_page = self.view.render("index", dict())
        return self.send_page(html_page, start_response)
