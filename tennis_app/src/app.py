from tennis_app.src.middlewares import (
    Dispatcher,
    StaticFileMiddleware,
    LoggingMiddleware,
)
from tennis_app.src.config.settings import STATIC_FILES_DIR

# app = LoggingMiddleware(
#     StaticFileMiddleware(
#         Dispatcher(), STATIC_FILES_DIR
#     )
# )

app = Dispatcher()
app = StaticFileMiddleware(app, STATIC_FILES_DIR)
app = LoggingMiddleware(app)
