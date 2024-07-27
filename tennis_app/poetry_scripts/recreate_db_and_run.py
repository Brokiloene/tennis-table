from .recreate_db import start as recreate_db
from .run_server import start as run_server

def start():
    recreate_db()
    run_server()