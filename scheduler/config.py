import os

from dotenv import load_dotenv

load_dotenv()


PG_DSN = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}

BROKER_HOST = os.getenv("BROKER_URL")
BROKER_DB = os.getenv("BROKER_DB")
BROKER_URL = f"{BROKER_HOST}/{BROKER_DB}"
EVENT_PRIORITY = os.getenv("EVENT_PRIORITY")
EVENT_LIMIT = os.getenv("EVENT_LIMIT")
RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_PORT = os.getenv("RABBITMQ_NODE_PORT")
RABBIT_USER = os.getenv("RABBIT_USERNAME")
RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD")
AMQP_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}/"
EXCHANGE = os.getenv("EXCHANGE")

log_config = {
    "sink": f"./log/{EVENT_PRIORITY}.log",
    "format": "{time} {level} {message}",
    "level": "INFO",
    "rotation": "00:00",
    "compression": "zip",
}
