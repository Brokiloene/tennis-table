from .response_status import Status

class BaseHandler:
    def send_error_response(self, start_response, status, headers, view):
        # response_headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        res = view("error-page", {"error_message": status})
        return [bytes(res, 'utf-8')]
        
    def send_response(self, start_response):
        status = "200 OK"
        self.response_headers.append(
            ('Content-Length', str(len(res)))
        )
        start_response(status, self.response_headers)
        return [bytes(res, 'utf-8')]

    #     # yield page
    
    # def get_tuple_send_args(
    #         self, 
    #         environ, 
    #         start_response, 
    #         msg, 
    #         headers,
    #         view, 
    #         **view_data):
    #     return (
    #         environ,
    #         start_response,
    #         msg,
    #         headers,
    #         view,
    #         view_data
    #     )

    status = Status()


    # def send_response(self, start_response, resp_status, headers, view, **view_data):
    #     headers.append(
    #         ('Content-Length', str(len(res)))
    #     )
    #     start_response(resp_status, headers)
    #     res = view(**view_data)
    #     return [bytes[res, 'utf-8']]
