import backoff
import psycopg2
from celery import Celery
from config import BROKER_URL, EVENT_LIMIT, EVENT_PRIORITY, PG_DSN, log_config
from loguru import logger
from psycopg2 import DatabaseError, OperationalError
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

logger.add(**log_config)

celery_app = Celery("tasks", broker=BROKER_URL)


class EventExtractor:
    """Класс для выгрузки событий из PostgreSQL."""

    def __init__(self, pg_conn: connection):
        self.cursor = pg_conn.cursor()

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=5)
    def get_event_uuids(self, event_type: str, limit: int):
        self.cursor.execute(
            f"""SELECT notification_id FROM events
            WHERE event_type = '{event_type}'
            AND in_queue = FALSE LIMIT {limit}"""
        )
        event_uuids = self.cursor.fetchall()
        if event_uuids:
            tuple_uuids = tuple([str(*_) for _ in event_uuids])
            self.cursor.execute(
                f"""UPDATE events SET in_queue = TRUE
                WHERE notification_id IN {tuple_uuids}"""
            )
            print(tuple_uuids)
            return event_uuids


@celery_app.task
def transfer_events():
    """
    Задача чтения UUID событий из базы.
    """

    try:
        with psycopg2.connect(
            dbname=PG_DSN["dbname"],
            user=PG_DSN["user"],
            password=PG_DSN["password"],
            host="postgres",
            cursor_factory=DictCursor,
        ) as pg_conn:
            pg = EventExtractor(pg_conn=pg_conn)
            pg.get_event_uuids(EVENT_PRIORITY, EVENT_LIMIT)
    except (OperationalError, DatabaseError) as e:
        logger.exception(e)


@celery_app.on_after_configure.connect
def setup_periodic_taskc(sender, **kwargs):
    """Планировщик запуска процессов (каждые 5 секунд)."""

    sender.add_periodic_task(5.0, transfer_events.s())
