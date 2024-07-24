from tennis_app.views import RendererHTML


class BaseHandler:
    def __init__(self) -> None:
        self.view = RendererHTML

    def send_error_page(self, environ, start_response, status):
        response_headers = [('Content-type', 'text/html')]
        start_response(status, response_headers)
        page = RendererHTML.render("error-page", {"error_message": status})
        return [bytes(page, 'utf-8')]

        # yield page
