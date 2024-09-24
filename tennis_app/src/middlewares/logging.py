import logging
import sys

from tennis_app.src.shared.core import BaseMiddleware
from tennis_app.src.shared.http_status import HttpStatus


logging.basicConfig(
    stream=sys.stdout, 
    level=logging.DEBUG, 
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

class LoggingMiddleware(BaseMiddleware):
    logger = logging.getLogger("tennis-app")

    def __call__(self, environ, start_response):
        self.logger.info(
            f"[INFO] Request: {environ['REQUEST_METHOD']} {environ['PATH_INFO']}"
            )

        def log_start_response(status, response_headers, logger=self.logger):
            logger.info(f"[INFO] Response: {status}\n")
            return start_response(status, response_headers)
        
        try:
            return self.app(environ, log_start_response)

        except Exception as e:
            self.logger.exception(e)
            self.send_error(start_response, HttpStatus.INTERNAL_ERROR)
