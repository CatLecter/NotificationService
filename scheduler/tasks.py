import psycopg2
from celery import Celery
from config import AMQP_URL, BROKER_URL, EVENT_LIMIT, EVENT_PRIORITY, PG_DSN, log_config
from extractor import EventExtractor
from loader import EventLoaderToQueue
from loguru import logger
from pika import BlockingConnection, URLParameters
from psycopg2 import DatabaseError, OperationalError
from psycopg2.extras import DictCursor

logger.add(**log_config)

celery_app = Celery("tasks", broker=BROKER_URL)


@celery_app.task
def transfer_events():
    """Задача трансфера notification_uuid из PostgreSQL в очередь событий RabbitMQ."""

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
            pg = EventExtractor(pg_conn=pg_conn)
            uuids = pg.get_event_uuids(EVENT_PRIORITY, EVENT_LIMIT)
            if uuids:
                amqp = EventLoaderToQueue(conn=amqp_conn)
                amqp.send_ids(uuids)
                pg.update_event_uuids(uuids)
    except (OperationalError, DatabaseError) as e:
        logger.exception(e)


@celery_app.on_after_configure.connect
def setup_periodic_taskc(sender, **kwargs):
    """Планировщик запуска процессов (каждые 10 секунд)."""

    sender.add_periodic_task(10.0, transfer_events.s())
