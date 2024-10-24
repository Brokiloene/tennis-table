from uuid import UUID

from tennis_app.src.shared.core import BaseController
from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.shared.dao import MemoryStorageDAO
from tennis_app.src.shared.serializers import MatchToDictSerializer
from .services.update_match import UpdateMatchService
from tennis_app.src.shared.http_status import HttpStatus
from .view import MainScoreView


class MatchScoreController(BaseController):
    def do_POST(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, "uuid"))
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)
        try:
            form_data = self.parse_post_form(environ)
        except ValueError:
            return self.send_error(
                start_response, HttpStatus.LENGTH_REQUIRED, self.headers
            )
        try:
            update_info = form_data["player-scores"][0]
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        try:
            view_data = UpdateMatchService.execute(match_uuid, update_info)
        except MatchNotFoundError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)
        data = MainScoreView.render(view_data)
        return self.send_response(start_response, self.headers, data)

    def do_GET(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, "uuid"))
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        try:
            match_obj = MemoryStorageDAO.read(match_uuid)
        except MatchNotFoundError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        view_data = MatchToDictSerializer.serialize(match_obj)
        data = MainScoreView.render(view_data)
        return self.send_response(start_response, self.headers, data)
