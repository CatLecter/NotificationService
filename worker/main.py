import psycopg2
from config import AMQP_URL, PG_DSN, log_config
from enricher import EventEnricher
from getter import EventGetter
from loguru import logger
from models import PrimaryData
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from psycopg2.extras import DictCursor

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
                    primary_data = PrimaryData(**pg.get_from_pg(uuid))
                    print(primary_data.data_endpoint)
    except AMQPConnectionError as e:
        logger.exception(e)


if __name__ == "__main__":
    worker()
