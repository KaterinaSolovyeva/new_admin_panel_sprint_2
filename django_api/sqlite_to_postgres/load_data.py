import contextlib
import sqlite3
from typing import Generator

import psycopg2
from dotenv import dotenv_values
from loaders import PostgresSaver, SQLiteExtractor
from psycopg2.extensions import connection as _connection
from tables import tables

DSN = dotenv_values('.envdsn')


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection) -> None:
    """The main method of loading data from SQLite to Postgres.
    Args:
        sqlite_conn: sqlite3 connection string
        pg_conn: Postgres connection string
    """
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(sqlite_conn)

    for table_name, table_dc in tables.items():
        sqlite_extractor.extract_movies(table_name, table_dc, postgres_saver)


@contextlib.contextmanager
def conn_context(db_path: str) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for sqlite with closing the connection.
    Arg:
        db_path: string path to the sqlite database
    Yields:
        conn: sqlite3 connection string
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


if __name__ == '__main__':
    with conn_context('db.sqlite') as sqlite_conn, contextlib.closing(
        psycopg2.connect(**DSN)
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
