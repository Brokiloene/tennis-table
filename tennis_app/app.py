from tennis_app.handlers import Dispatcher
from tennis_app.handlers.middlewares import StaticFileMiddleware, LoggingMiddleware

app = Dispatcher()
app = StaticFileMiddleware(app, './tennis_app/static')
app = LoggingMiddleware(app)
