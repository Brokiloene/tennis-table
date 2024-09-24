from tennis_app.src.shared.http_status import HttpStatus
from tennis_app.src.shared.view.error_view import ErrorView

class BaseHandler:
    def send_response(self, start_response, headers, data):
        headers.append(
            ('Content-Length', str(len(data)))
        )
        start_response(HttpStatus.OK, headers)
        return [bytes(data, 'utf-8')]

    def send_error(self, start_response, status, headers):
        return self.send_response(
            start_response,
            status,
            headers,
            ErrorView({"error_message": status})    
        )
