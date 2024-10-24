from tennis_app.src.shared.core import BaseController
from tennis_app.src.shared.exceptions import PaginationError
from .services.match_history import MatchHistoryService
from tennis_app.src.shared.http_status import HttpStatus
from .view import MatchHistoryView


class MatchesHistoryController(BaseController):
    def do_GET(self, environ, start_response):
        try:
            cur_page = int(self.get_query_param(environ, "page"))
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)
        try:
            search_name = self.get_query_param(environ, "filter_by_player_name")
        except KeyError:
            search_name = None

        try:
            cur_page, max_page, all_matches = MatchHistoryService.get_matches(
                search_name, cur_page, MatchHistoryView.MATCHES_ON_ONE_PAGE
            )
        except PaginationError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        match_data = MatchHistoryView.get_matches_template_data(
            all_matches=all_matches, cur_page=cur_page, max_page=max_page
        )
        data = MatchHistoryView.render(match_data)

        return self.send_response(start_response, self.headers, data)
