import waitress
from app import app

def start():
    waitress.serve(app, host="127.0.0.1", port="2000")
