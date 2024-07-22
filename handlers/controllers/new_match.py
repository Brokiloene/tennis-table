from services import MatchService
from utils import UUID
from exceptions import PlayerNamesAreTheSameError
from .base import BaseController

class NewMatchController(BaseController):
    def do_GET(self, environ, start_response):
        status = "200 OK"
        page = self.view.render("new-match", dict())
        self.response_headers.append(
            ('Content-Length', str(len(page)))
        )
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
    
    def do_POST(self, environ, start_response):
        try:
            form_data = self.parse_post_form(environ)
        except ValueError:
            return self.send_error(environ, start_response, "411 Length Required")
        try:
            player1_name: str = form_data['name-p1'][0]
            player2_name: str = form_data['name-p2'][0]
        except KeyError:
            return self.send_error(environ, start_response, "400 Bad Request")
        
        try:
            match_uuid: UUID = MatchService.create_match(player1_name, player2_name)
        except PlayerNamesAreTheSameError:
            return self.send_error(environ, start_response, "400 Bad Request")

        status = '303 See other'
        self.response_headers.append(('Location', f'/match-score?uuid={str(match_uuid)}'))
        page = 'Redirecting...'
        self.response_headers.append(
            ('Content-Length', str(len(page)))
        )
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
