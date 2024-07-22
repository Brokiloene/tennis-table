from .database import session_factory
from .match import MatchModel
from .player import PlayerModel
from .database import engine, BaseModel

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="user",
    passwd="pass"
)

curs = db.cursor()
try:
    curs.execute("DROP DATABASE tennis_db")
except mysql.connector.errors.DatabaseError:
    pass
finally:
    curs.execute("CREATE DATABASE tennis_db")
    curs.execute("SHOW DATABASES")

# with engine.connect() as conn:
#     conn.execute("DROP DATABASE db")
#     conn.execute("CREATE DATABASE db")
#     conn.execute("USE dbname")
BaseModel.metadata.create_all(engine)
