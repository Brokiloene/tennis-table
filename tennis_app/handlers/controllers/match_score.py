from typing import Dict

from tennis_app.services import MatchService
from tennis_app.utils import UUID
from tennis_app.exceptions import MatchNotFoundError
from .base import BaseController


class MatchScoreController(BaseController):
    def do_POST(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, 'uuid'))
        except KeyError:
            return self.send_error_page(environ, start_response, '400 Bad Request')

        form_data: Dict = self.parse_post_form(environ)

        try:
            if "p1-scores" in form_data:
                MatchService.match_add_point(match_uuid, 1)
            elif "p2-scores" in form_data:
                MatchService.match_add_point(match_uuid, 2)
        except MatchNotFoundError:
            return self.send_error_page(environ, start_response, '400 Bad Request')

        view_data: Dict[str, str] = MatchService.get_match_data(match_uuid)

        if view_data["match_status"] == "match is over":
            MatchService.save_finished_match(match_uuid)

        html_page = self.view.render("match-score", view_data)
        return self.send_page(html_page, start_response)
  
    
    def do_GET(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, 'uuid'))
        except KeyError:
            return self.send_error_page(environ, start_response, '400 Bad Request')

        try:
            view_data = MatchService.get_match_data(match_uuid)        
        except MatchNotFoundError:
            return self.send_error_page(environ, start_response, '400 Bad Request')
        
        html_page = self.view.render("match-score", view_data)
        return self.send_page(html_page, start_response)
     