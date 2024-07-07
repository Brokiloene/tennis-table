from .base import BaseController


class MatchScoreController(BaseController):
    def do_POST(self, environ, start_response):
        pass
    
    def do_GET(self, environ, start_response):
        print(environ)
        try:
            data = {
                "name_p1": environ['form_data']['name-p1'][0],
                "name_p2": environ['form_data']['name-p2'][0]
            }
            data = self.view.score_data_template | data

        except KeyError:
            return self.send_error(environ, start_response, "422 Unprocessable Entity")
        
        page = self.view.render("match-score", data)
        status = "200 OK"
        start_response(status, self.response_headers)
        return [bytes(page, 'utf-8')]
