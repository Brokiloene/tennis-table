FROM python:3.10-slim

WORKDIR /home/app

COPY pyproject.toml .

RUN pip install poetry
RUN poetry install --no-root

COPY . .
RUN chmod +x ./startup_commands.sh

ENTRYPOINT ["./startup_commands.sh"]