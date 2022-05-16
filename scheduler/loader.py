import uuid
from pickle import dumps

import backoff
from config import EVENT_PRIORITY
from pika import BlockingConnection
from pika.exceptions import AMQPConnectionError


class EventLoaderToQueue:
    """Класс для загрузки событий в RabbitMQ."""

    def __init__(self, conn: BlockingConnection):
        self.conn = conn
        self.channel = self.conn.channel()

    @backoff.on_exception(backoff.expo, AMQPConnectionError, max_tries=5)
    def send_ids(self, list_uuids: tuple) -> None:
        for _uuid in list_uuids:
            self.channel.basic_publish(
                exchange=EVENT_PRIORITY,
                routing_key=str(uuid.uuid4()),
                body=dumps(_uuid),
            )
