import backoff
import requests
from loguru import logger
from models import Film, PrimaryData, User
from psycopg2 import OperationalError
from psycopg2.extensions import connection
from pydantic import BaseModel
from requests import HTTPError

from .config import DEPARTURE_ADDRESS, log_config

logger.add(**log_config)


class EventEnricher:
    """Класс для обогащения данными событий из очереди."""

    def __init__(self, pg_conn: connection):
        self.cursor = pg_conn.cursor()

    @backoff.on_exception(backoff.expo, OperationalError, max_tries=5)
    def enrich(self, event_uuid: str) -> PrimaryData:
        self.cursor.execute(
            f"""SELECT * FROM events WHERE notification_id = '{event_uuid}'"""
        )
        data = self.cursor.fetchone()
        return PrimaryData(**data)

    def get_user(self, endpoint: str) -> User:
        user_data = requests.get(endpoint)
        return User(**user_data.json())

    def get_film(self, endpoint: str) -> Film:
        film_data = requests.get(endpoint)
        return Film(**film_data.json())

    def give(self, data: BaseModel) -> None:
        try:
            requests.post(url=DEPARTURE_ADDRESS, json=data.json())
        except HTTPError as e:
            print(e)
            logger.exception(e)

    def processing(self, data: BaseModel) -> None:
        pass
