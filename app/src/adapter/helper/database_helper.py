import psycopg2
import logging

from app.src.util.singleton_meta import SingletonMeta
from app.src.adapter.helper.os_helper import OsHelper

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DatabaseHelper(metaclass=SingletonMeta):
    _connection = None

    def __init__(self):
        self._connection = DatabaseHelper.__connect(
            OsHelper.get_required_env("POINT_DB_HOST"),
            OsHelper.get_required_env("POINT_DB_DATABASE"),
            OsHelper.get_required_env("POINT_DB_USERNAME"),
            OsHelper.get_required_env("POINT_DB_PASSWORD")
        )

    def __del__(self):
        if self._connection:
            self._connection.close()
            print("db connection closed.")

    @staticmethod
    def __connect(host, database, user, password):
        try:
            connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )

            connection.autocommit = True

            return connection

        except psycopg2.Error as e:
            logging.error("Error connecting to database.")
            raise Exception("Error connecting to database.", e)

    @staticmethod
    def __rows_to_dict(cursor, rows):
        rows_dict = []

        for row in rows:
            row_dict = DatabaseHelper.__row_to_dict(cursor, row)
            rows_dict.append(row_dict)

        return rows_dict

    @staticmethod
    def __row_to_dict(cursor, row):
        logging.info(f"row: {row}")
        column_names = [desc[0] for desc in cursor.description]
        return dict(zip(column_names, row))

    def fetch_all(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return self.__rows_to_dict(cursor, rows)

        except psycopg2.Error as e:
            logging.error("Error executing query '%s' with parameters '%s'", query, params)
            raise Exception("Error executing query.", e)

    def fetch_one(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                logging.info("Executing query '%s' with parameters '%s'", query, params)
                cursor.execute(query, params)
                row = cursor.fetchone()
                return self.__row_to_dict(cursor, row)

        except psycopg2.Error as e:
            logging.error("Error executing query '%s' with parameters '%s'", query, params)
            raise Exception("Error executing query.", e)

    def insert_or_update(self, query, params=None):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                self._connection.commit()

        except psycopg2.Error as e:
            logging.error("Error executing query '%s' with parameters '%s'", query, params)
            raise Exception("Error executing query.", e)
