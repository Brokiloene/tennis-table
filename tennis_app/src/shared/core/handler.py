from tennis_app.src.shared.http_status import HttpStatus
from tennis_app.src.shared.view import ErrorView


class BaseHandler:
    def send_response(self, start_response, headers, data, status=HttpStatus.OK):
        start_response(status, headers + [("Content-Length", str(len(data)))])
        return [bytes(data, "utf-8")]

    def send_error(self, start_response, status, headers):
        return self.send_response(
            start_response, headers, ErrorView.render({"error_message": status})
        )
