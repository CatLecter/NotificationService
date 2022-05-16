import backoff
from psycopg2 import OperationalError
from psycopg2.extensions import connection


class EventEnricher:
    """Класс для обогащения данными событий из очереди."""

    def __init__(self, pg_conn: connection):
        self.cursor = pg_conn.cursor()

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=5)
    def get_from_pg(self, event_uuid: str):
        # TODO: исправить передачу события в скрипт
        self.cursor.execute(
            f"""SELECT * FROM events WHERE notification_id = '{event_uuid}'"""
        )
        return self.cursor.fetchone()

    def get_from_endpoint(self):
        # http://0.0.0.0/api/v1/movies/4bc17ed1-010c-4ff9-8f95-d5de21be6c60/view
        # http://0.0.0.0/api/v1/movies/29a2afcf-0058-41ef-92c8-0497bffa77a2/bookmark

        pass
