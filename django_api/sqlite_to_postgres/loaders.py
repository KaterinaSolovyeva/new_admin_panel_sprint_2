import sqlite3
from dataclasses import fields
from typing import List, Optional, Union

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
from tables import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork

BATCH_SIZE = 1000


class PostgresSaver:
    """Records to Postgres data"""

    def __init__(self, pg_conn: _connection):
        """Initialize postgres saver.
        Args:
            pg_conn: Postgres connection string
        """
        self.pg_conn = pg_conn

    @staticmethod
    def get_insert_query(
        table_name: str,
        table_dc: Union[Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork]
    ) -> str:
        """Returns sql to insert data with UPSERT.
        Args:
            table_name: table name string
            table_dc: dataclass fields - columns of table
        Return:
            sql string
        """
        field = [field.name for field in fields(table_dc)]
        values = ('%s, ' * len(field)).rstrip(', ')
        return (
            'INSERT INTO {table} ({columns}) VALUES ({values}) '
            'ON CONFLICT DO NOTHING;'.format(
                columns=', '.join(field),
                table=table_name,
                values=values
            )
        )

    def save_all_data(
        self,
        data: List[Optional[sqlite3.Row]],
        table_name: str,
        table_dc: Union[Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork]
    ) -> None:
        """Insert data to Postgres tables.
        Args:
            data: data from sqlite base
            table_name: table name in postgres base
            table_dc: dataclass fields - columns of table
        """
        cur = self.pg_conn.cursor()
        query = self.get_insert_query(table_name, table_dc)
        execute_batch(cur, query, data, page_size=BATCH_SIZE)
        self.pg_conn.commit()


class SQLiteExtractor:
    """Extracts data from SQLite"""

    def __init__(self, sqlite_conn: sqlite3.Connection):
        """Initialize of loader.
        Args:
            sqlite_conn: sqlite3 connection string
        """
        self.conn = sqlite_conn

    @staticmethod
    def get_select_query(
        table_name: str,
        table_dc: Union[Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork]
    ) -> str:
        """Returns sql to get necessary data.
        Args:
            table_name: table name string
            table_dc: dataclass fields - columns of table
        Return:
            sql string
        """
        field = [field.name for field in fields(table_dc)]
        return 'SELECT {columns} FROM {table};'.format(
            columns=', '.join(field),
            table=table_name
        )

    def extract_movies(
        self,
        table_name: str,
        table_dc: Union[Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork],
        postgres_saver: PostgresSaver
    ):
        """Selects data from sqlite3 and sends to PostgresSaver to save.
        Args:
            table_name: table name string
            table_dc: dataclass fields - columns of table
            postgres_saver: instance of PostgresSaver
        """
        curs = self.conn.cursor()
        curs.execute(self.get_select_query(table_name, table_dc))
        while True:
            data = curs.fetchmany(BATCH_SIZE)
            if not data:
                break
            postgres_saver.save_all_data(data, table_name, table_dc)
