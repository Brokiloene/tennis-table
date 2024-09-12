import waitress
from tennis_app.app import app

def start():
    waitress.serve(app, host="0.0.0.0", port="2000")
