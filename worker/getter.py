from pickle import loads
from typing import Generator

import backoff
from config import QUEUE
from pika import BlockingConnection
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker


class EventGetter:
    """Класс для получения событий из RabbitMQ."""

    def __init__(self, conn: BlockingConnection):
        self.conn = conn
        self.channel = self.conn.channel()

    @backoff.on_exception(backoff.expo, AMQPConnectionError, max_tries=5)
    def get_uuid(self) -> Generator:
        try:
            for method_frame, properties, body in self.channel.consume(QUEUE):
                yield loads(body)
                self.channel.basic_ack(method_frame.delivery_tag)
        except ChannelClosedByBroker:
            self.channel.cancel()
        finally:
            self.channel.cancel()
