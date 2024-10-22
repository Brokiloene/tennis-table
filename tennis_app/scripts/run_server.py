import waitress
from tennis_app.src.app import app

def start():
    waitress.serve(app, host="0.0.0.0", port="1280")
