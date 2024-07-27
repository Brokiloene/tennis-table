from math import ceil

from tennis_app.services import MatchesHistoryService
from .base import BaseController

class MatchesHistoryController(BaseController):    
    def do_GET(self, environ, start_response):
        try:
            query_string = environ.get('QUERY_STRING', '')
            cur_page = int(self.get_query_param(environ, 'page'))
        except KeyError:
            print(query_string)
            return self.send_error_page(environ, start_response, "400 Bad Request")
        try:
            search_name = self.get_query_param(environ, 'filter_by_player_name')
        except KeyError:
            search_name = None
        
        if search_name is not None:
            all_matches = MatchesHistoryService.get_matches_filtered_by_name(search_name)
        else:
            all_matches = MatchesHistoryService.get_all_matches()

        max_page=max(ceil( len(all_matches)/2 ), 1)

        if cur_page < 1:
            cur_page = 1
        if cur_page > max_page:
            cur_page = max_page

        if len(all_matches)+1 < cur_page*2 and len(all_matches) != 0:
            return self.send_error_page(environ, start_response, "400 Bad Request")

        html_page = self.view.render("matches", self.view.get_matches_template_data(
            all_matches=all_matches,
            cur_page=cur_page,
            max_page=max_page
            ))
        return self.send_page(html_page, start_response)
