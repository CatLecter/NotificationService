import backoff
from psycopg2 import OperationalError
from psycopg2.extensions import connection


class EventExtractor:
    """Класс для выгрузки событий из PostgreSQL."""

    def __init__(self, pg_conn: connection):
        self.cursor = pg_conn.cursor()

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=5)
    def get_event_uuids(self, event_type: str, limit: int) -> tuple:
        self.cursor.execute(
            f"""SELECT notification_id FROM events
            WHERE event_type = '{event_type}'
            AND in_queue = FALSE LIMIT {limit}"""
        )
        list_uuids = self.cursor.fetchall()
        tuple_uuids = tuple(str(*_) for _ in list_uuids)
        return tuple_uuids

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=5)
    def update_event_uuids(self, tuple_uuids: tuple) -> None:
        self.cursor.execute(
            f"""UPDATE events SET in_queue = TRUE
            WHERE notification_id IN {tuple_uuids}"""
        )
