from tennis_app.src.middlewares import (
    Dispatcher, 
    StaticFileMiddleware, 
    LoggingMiddleware
)
from tennis_app.src.views import RendererHTML
from tennis_app.src.config.settings import STATIC_FILES_DIR

app = Dispatcher(view=RendererHTML)
app = StaticFileMiddleware(app, STATIC_FILES_DIR)
app = LoggingMiddleware(app)
