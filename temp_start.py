import poetry_scripts.create_db
import poetry_scripts.fill_db
import poetry_scripts.run_server

poetry_scripts.create_db.start()

import subprocess
subprocess.run("alembic upgrade head", shell=True)

poetry_scripts.fill_db.start()
poetry_scripts.run_server.start()
