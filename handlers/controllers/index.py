from .base import BaseController

class IndexController(BaseController):

    def do_GET(self, environ, start_response):
        status = "200 OK"
        html_page = self.view.render("index", dict())
        self.response_headers.append(
            ('Content-Length', str(len(html_page)))
        )
        start_response(status, self.response_headers)
        return [bytes(html_page, 'utf-8')]
