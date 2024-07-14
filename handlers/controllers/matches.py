from .base import BaseController

class MatchesHistoryController(BaseController):    
    def do_GET(self, environ, start_response):
        status = "200 OK"
        page = self.view.render("matches", dict())
        self.response_headers.append(
            ('Content-Length', str(len(page)))
        )
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
