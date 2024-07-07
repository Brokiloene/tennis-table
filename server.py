import waitress

from handlers import Dispatcher
from handlers.middlewares import StaticFileMiddleware, LoggingMiddleware


app = Dispatcher()
app = StaticFileMiddleware(app, './static')
app = LoggingMiddleware(app)


if __name__ == '__main__':
    waitress.serve(app, host="127.0.0.1", port="2000")

