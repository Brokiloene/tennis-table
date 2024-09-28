from math import ceil

from tennis_app.src.shared.core import BaseController
from .services.matches_history import MatchesHistoryService
from tennis_app.src.shared.http_status import HttpStatus
from .ui.view import MatchHistoryView


class MatchesHistoryController(BaseController):    
    def do_GET(self, environ, start_response):
        try:
            cur_page = int(self.get_query_param(environ, 'page'))
        except KeyError:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)
        try:
            search_name = self.get_query_param(environ, 'filter_by_player_name')
        except KeyError:
            search_name = None
        
        # Move this to SearchMatchByNameService
        if search_name is None:
            all_matches = MatchesHistoryService.get_all_matches()
        else:
            all_matches = MatchesHistoryService.get_matches_filtered_by_name(search_name)
        
        max_page=max(ceil(len(all_matches)/2), 1)

        if cur_page < 1:
            cur_page = 1
        if cur_page > max_page:
            cur_page = max_page

        if len(all_matches)+1 < cur_page*2 and len(all_matches) != 0:
            return self.send_error(start_response, HttpStatus.BAD_REQUEST, self.headers)

        match_data = MatchHistoryView.get_matches_template_data(
            all_matches=all_matches,
            cur_page=cur_page,
            max_page=max_page
            )
        data = MatchHistoryView.render(data)
        
        return self.send_response(start_response, self.headers, data)
