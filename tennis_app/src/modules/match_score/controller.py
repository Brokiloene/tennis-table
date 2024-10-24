from uuid import UUID

from tennis_app.src.shared.core import BaseController
from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.shared.dao import MemoryStorageDAO
from tennis_app.src.shared.serializers import MatchToDictSerializer
from tennis_app.src.shared.tennis_game_logic import Match
from tennis_app.src.shared.http_status import HttpStatus
from .services.update_match import UpdateMatchService
from .view import MainScoreView


class MatchScoreController(BaseController):
    def do_POST(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, "uuid"))
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)
        try:
            form_data: dict[str, list[str]] = self.parse_post_form(environ)
        except ValueError:
            return self.send_error(
                start_response, HttpStatus.LENGTH_REQUIRED, self.headers
            )
        try:
            update_info: str = form_data["player-scores"][0]
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        try:
            view_data: dict[str, str] = UpdateMatchService.execute(
                match_uuid, update_info
            )
        except MatchNotFoundError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)
        data: str = MainScoreView.render(view_data)
        return self.send_response(start_response, self.headers, data)

    def do_GET(self, environ, start_response):
        try:
            match_uuid = UUID(self.get_query_param(environ, "uuid"))
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        try:
            match_: Match = MemoryStorageDAO.read(match_uuid)
        except MatchNotFoundError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        view_data: dict[str, str] = MatchToDictSerializer.serialize(match_)
        data: str = MainScoreView.render(view_data)
        return self.send_response(start_response, self.headers, data)
