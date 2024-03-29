from json.decoder import JSONDecodeError

import backoff
import requests
from config import DEPARTURE_ADDRESS, log_config
from loguru import logger
from models import Film, PrimaryData, User
from psycopg2 import OperationalError
from psycopg2.extensions import connection
from pydantic import BaseModel
from requests import HTTPError

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
        if data:
            return PrimaryData(**data)

    def get_user(self, endpoint: str) -> User:
        user_data = requests.get(endpoint)
        return User(**user_data.json())

    @backoff.on_exception(backoff.expo, (JSONDecodeError, AssertionError), max_tries=5)
    def get_film(self, endpoint: str) -> Film:
        film_data_response = requests.get(endpoint)
        assert film_data_response.status == 200, "Bad response!"
        return Film(**film_data_response.json())

    def give(self, data: BaseModel) -> None:
        try:
            requests.post(url=DEPARTURE_ADDRESS, json=data.json())
        except HTTPError as e:
            logger.exception(e)
