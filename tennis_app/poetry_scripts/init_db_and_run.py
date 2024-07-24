from .init_db import start as init_db_start
from .run_server import start as run_server_start

def start():
    init_db_start()
    run_server_start()