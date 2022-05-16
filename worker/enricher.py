import backoff
import requests
from models import AbridgedFilm, Film, PrimaryData, ResponseFilms, ResponseUser, User
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

    def get_user(self, endpoint: str, action: str) -> ResponseUser:
        user_data = requests.get(endpoint)
        user = User(**user_data.json())
        return ResponseUser(action=action, user=user)

    def get_films(self, endpoint: str, source: str) -> ResponseFilms:
        film_data = requests.get(endpoint)
        film = Film(**film_data.json())
        abridged_film = AbridgedFilm(
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        return ResponseFilms(source=source, films=abridged_film)
