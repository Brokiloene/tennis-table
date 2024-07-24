from math import ceil

from services import MatchesHistoryService
from .base import BaseController

class MatchesHistoryController(BaseController):    
    def do_GET(self, environ, start_response):
        try:
            cur_page = int(self.get_query_param(environ, 'page'))
        except KeyError:
            return self.send_error_page(environ, start_response, "400 Bad Request")
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
