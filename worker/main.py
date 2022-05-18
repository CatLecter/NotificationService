import psycopg2
from config import AMQP_URL, PG_DSN, log_config
from enricher import EventEnricher
from getter import EventGetter
from loguru import logger
from models import ResponseModel
from pika import BlockingConnection, URLParameters
from pika.exceptions import AMQPConnectionError
from psycopg2.extras import DictCursor

logger.add(**log_config)


def process_uuid(pg: EventEnricher, uuid):
    # т.к. нам нужно обрабатывать и срочные события, то ждать получения целой пачки UUID
    # чтобы сходить за ними в базу не представляется возможным, воркер должен уметь
    # обратывать одно конкретное событие, а если он не справляется, то всегда можно
    # поднять ещё один сконфигурировав docker-compose.yml
    primary_data = pg.enrich(uuid)
    if primary_data:
        if primary_data.source == "UGC":
            film_data = pg.get_film(
                endpoint=primary_data.data_endpoint,
            )
            user_data = pg.get_user(
                endpoint=primary_data.data_endpoint,
            )
            data = ResponseModel(
                email=user_data.email,
                templates_type=primary_data.action,
                data=film_data.dict(),
            )
            pg.give(data)
        if any([(primary_data == "USER"), (primary_data == "ADMIN")]):
            _user_data = pg.get_user(
                endpoint=primary_data.data_endpoint,
            )
            data = ResponseModel(
                email=_user_data.email,
                templates_type=primary_data.action,
                data=_user_data.dict(),
            )
            pg.give(data)


def amqp_conn_worker(amqp_conn: BlockingConnection, pg_conn) -> None:
    amqp = EventGetter(conn=amqp_conn)
    uuids = amqp.get_uuid()
    pg = EventEnricher(pg_conn)
    for uuid in uuids:
        process_uuid(pg, uuid)


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
                amqp_conn_worker(amqp_conn, pg_conn)

    except AMQPConnectionError as e:
        logger.exception(e)


if __name__ == "__main__":
    worker()
