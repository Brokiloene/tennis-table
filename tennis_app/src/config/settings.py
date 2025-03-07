import os
from dotenv import load_dotenv

load_dotenv()
DB_DRIVER = os.getenv("DB_DRIVER")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TEMPLATES_DIR = "./tennis_app/src/templates"
STATIC_FILES_DIR = "./tennis_app/public"

MEMORY_STORAGE_CAPACITY = 128
