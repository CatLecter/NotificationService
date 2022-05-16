import backoff
from models import Film, PrimaryData, User
from psycopg2 import OperationalError
from psycopg2.extensions import connection


class EventEnricher:
    """Класс для обогащения данными событий из очереди."""

    def __init__(self, pg_conn: connection):
        self.cursor = pg_conn.cursor()

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=5)
    def enrich(self, event_uuid: str) -> PrimaryData:
        # TODO: исправить передачу события в скрипт
        self.cursor.execute(
            f"""SELECT * FROM events WHERE notification_id = '{event_uuid}'"""
        )
        data = self.cursor.fetchone()
        return PrimaryData(**data)

    def get_user(self, endpoint: str) -> User:
        # Ручкв для получения дополнительных данных.
        # http://0.0.0.0/api/v1/users/{UUID}

        return User()

    def get_film(self, endpoint: str) -> Film:
        # Ручка для получения дополнительных данных.
        # http://0.0.0.0/api/v1/films/{UUID}

        return Film()
