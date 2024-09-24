from typing import Dict
from uuid import UUID

from tennis_app.src.shared.core import BaseController
from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.shared.dao import MemoryStorageDAO
from tennis_app.src.shared.serializers import MatchToDictSerializer
from .services.save_match import SaveMatchService
from tennis_app.src.views import htmlView


class MatchScoreController(BaseController):
    def do_POST(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, 'uuid'))
        except KeyError:
            return self.send_error_response(environ, start_response, '400 Bad Request', htmlView)
        try:
            form_data = self.parse_post_form(environ)
        except ValueError:
            return self.send_error_response(environ, start_response, "411 Length Required", htmlView)
        
        try:
            if "p1-scores" in form_data:
                MemoryStorageDAO.update(match_uuid, 1)
            elif "p2-scores" in form_data:
                MemoryStorageDAO.update(match_uuid, 2)

            match_obj = MemoryStorageDAO.read(match_uuid)
            view_data = MatchToDictSerializer.serialize(match_obj)
            if view_data["match_status"] == "match is over":
                SaveMatchService.execute(match_uuid)
        except MatchNotFoundError:
            return self.send_error_response(environ, start_response, '400 Bad Request', htmlView)
        
        res = htmlView("match-score", view_data)
        return self.send_response(res, start_response)
  
    
    def do_GET(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, 'uuid'))
        except KeyError:
            return self.send_error_response(environ, start_response, '400 Bad Request', htmlView)

        try:
            match_obj = MemoryStorageDAO.read(match_uuid)
        except MatchNotFoundError:
            return self.send_error_response(environ, start_response, '400 Bad Request')
        
        view_data = MatchToDictSerializer.serialize(match_obj)
        res = htmlView("match-score", view_data)
        return self.send_response(res, start_response)
