#!/bin/bash
poetry run alembic upgrade head
poetry run test_fill_db
poetry run run_server