FROM python:3.10-slim

WORKDIR /home/app
COPY . .

RUN pip install poetry &&\
    poetry install
RUN chmod +x ./commands.sh
ENTRYPOINT ["./commands.sh"]