from math import ceil

from services import MatchesHistoryService
from .base import BaseController

class MatchesHistoryController(BaseController):    
    def do_GET(self, environ, start_response):
        status = "200 OK"

        cur_page = int(self.get_query_param(environ, 'page'))
        all_matches = MatchesHistoryService.get_all_matches()
        max_page=max(ceil( len(all_matches)/2 ), 1)

        if cur_page < 1:
            cur_page = 1
        if cur_page > max_page:
            cur_page = max_page

        if len(all_matches)+1 < cur_page*2 and len(all_matches) != 0:
            return self.send_error(environ, start_response, "400 Bad Request")

        print(all_matches, cur_page, ceil(len(all_matches)/2))
        html_page = self.view.render("matches", self.view.get_matches_template_data(
            all_matches=all_matches,
            cur_page=cur_page,
            max_page=max_page
            ))
        self.response_headers.append(
            ('Content-Length', str(len(html_page)))
        )
        start_response(status, self.response_headers)
        return [bytes(html_page, 'utf-8')]
