from uuid import UUID

from tennis_app.src.shared.core import BaseController
from tennis_app.src.shared.dao import MemoryStorageDAO
from tennis_app.src.shared.exceptions import MatchNotFoundError

class NewMatchController(BaseController):
    def do_GET(self, environ, start_response):
        res = htmlView("new-match", {})
        return self.send_response(res, start_response)
    
    def do_POST(self, environ, start_response):
        try:
            form_data = self.parse_post_form(environ)
        except ValueError:
            return self.send_error_response(environ, start_response, "411 Length Required")
        try:
            player1_name: str = form_data['name-p1'][0]
            player2_name: str = form_data['name-p2'][0]
        except KeyError:
            return self.send_error_response(environ, start_response, "400 Bad Request")
        
        match_uuid: UUID = MemoryStorageDAO.create(player1_name, player2_name)

        return self.redirect_to(f'/match-score?uuid={str(match_uuid)}', start_response)
