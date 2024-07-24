from sqlalchemy_utils import database_exists, create_database
from models import engine

def start():
    if not database_exists(engine.url):
        create_database(engine.url)
