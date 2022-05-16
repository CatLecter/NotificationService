import psycopg2
import requests
from enricher import EventEnricher
from getter import EventGetter
from loguru import logger
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from psycopg2.extras import DictCursor

from .config import AMQP_URL, PG_DSN, log_config

logger.add(**log_config)


def worker():
    try:
        with psycopg2.connect(
            dbname=PG_DSN["dbname"],
            user=PG_DSN["user"],
            password=PG_DSN["password"],
            host=PG_DSN["host"],
            cursor_factory=DictCursor,
        ) as pg_conn, BlockingConnection(
            URLParameters(AMQP_URL),
        ) as amqp_conn:
            while True:
                amqp = EventGetter(conn=amqp_conn)
                uuids = amqp.get_uuid()
                pg = EventEnricher(pg_conn)
                for uuid in uuids:
                    primary_data = pg.enrich(uuid)
                    if primary_data.source == "USER" or "ADMIN":
                        user_data = pg.get_user(
                            endpoint=primary_data.data_endpoint,
                            action=primary_data.action,
                        )
                        requests.post(url="url...", json=user_data.json())
                    if primary_data.source == "UGC":
                        films_data = pg.get_films(
                            endpoint=primary_data.data_endpoint,
                            source=primary_data.source,
                        )
                        requests.post(url="url...", json=films_data.json())
    except AMQPConnectionError as e:
        logger.exception(e)


if __name__ == "__main__":
    worker()
