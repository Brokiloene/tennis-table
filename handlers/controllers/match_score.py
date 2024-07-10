from urllib.parse import urlparse, parse_qs

from services import MatchService
from .base import BaseController


class MatchScoreController(BaseController):
    def do_POST(self, environ, start_response):
        try:
            match = self.get_match_by_uuid(environ)
        except KeyError:
            return self.send_error(environ, start_response, '400 Bad Request')

        form_data = self.parse_post_form(environ)
        if "p1-scores" in form_data:
            match.add_game_point(1)
        elif "p2-scores" in form_data:
            match.add_game_point(2)
        else:
            return self.send_error(environ, start_response, '400 Bad Request')

        view_data = match.serialize()
        page = self.view.render("match-score", view_data)
        status = "200 OK"
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
  
    
    def do_GET(self, environ, start_response):
        try:
            match = self.get_match_by_uuid(environ)
        except KeyError:
            return self.send_error(environ, start_response, '400 Bad Request')
        
        view_data = match.serialize()

        # data = self.view.score_data_template | data

        page = self.view.render("match-score", view_data)
        status = "200 OK"
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
    
    def get_match_by_uuid(self, environ):
        query = environ['QUERY_STRING']
        match_uuid = parse_qs(query)['uuid'][0]
        return MatchService.ongoing_matches[match_uuid]
        
