from urllib.parse import parse_qs
from typing import Dict

from services import MatchService
from utils import UUID
from exceptions import MatchNotFoundError
from .base import BaseController


class MatchScoreController(BaseController):
    def do_POST(self, environ, start_response):
        try:
            match_uuid: UUID = self.get_match_uuid(environ)
        except KeyError:
            return self.send_error(environ, start_response, '400 Bad Request')

        form_data: Dict = self.parse_post_form(environ)

        try:
            if "p1-scores" in form_data:
                MatchService.match_add_point(match_uuid, 1)
            elif "p2-scores" in form_data:
                MatchService.match_add_point(match_uuid, 2)
        except MatchNotFoundError:
            return self.send_error(environ, start_response, '400 Bad Request')

        view_data: Dict[str, str] = MatchService.get_match_data(match_uuid)

        if view_data["match_status"] == "match is over":
            MatchService.save_finished_match(match_uuid)

        page = self.view.render("match-score", view_data)
        status = "200 OK"
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
  
    
    def do_GET(self, environ, start_response):
        try:
            match_uuid: UUID = self.get_match_uuid(environ)
        except KeyError:
            return self.send_error(environ, start_response, '400 Bad Request')

        try:
            view_data = MatchService.get_match_data(match_uuid)        
        except MatchNotFoundError:
            return self.send_error(environ, start_response, '400 Bad Request')
        
        page = self.view.render("match-score", view_data)
        status = "200 OK"
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
     
    def get_match_uuid(self, environ) -> UUID:
        query = environ['QUERY_STRING']
        uuid_str = parse_qs(query)['uuid'][0]
        return UUID(uuid_str)
