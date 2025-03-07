from uuid import UUID

from tennis_app.src.shared.core import BaseController
from tennis_app.src.shared.dao import MemoryStorageDAO
from tennis_app.src.shared.http_status import HttpStatus
from .view import NewMatchView


class NewMatchController(BaseController):
    def do_GET(self, environ, start_response):
        data = NewMatchView.render({})
        return self.send_response(start_response, self.headers, data)

    def do_POST(self, environ, start_response):
        try:
            form_data: dict[str, list[str]] = self.parse_post_form(environ)
        except ValueError:
            return self.send_error(
                start_response, HttpStatus.LENGTH_REQUIRED, self.headers
            )
        try:
            player1_name: str = form_data["name-p1"][0]
            player2_name: str = form_data["name-p2"][0]
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        match_uuid: UUID = MemoryStorageDAO.create(player1_name, player2_name)

        return self.redirect_to(
            f"/match-score?uuid={str(match_uuid)}", start_response, self.headers
        )
