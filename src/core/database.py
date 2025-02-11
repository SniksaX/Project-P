import psycopg2
from psycopg2 import sql
from core.config import settings


class DatabaseManager:
    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=settings.DATABASE_HOST,
            dbname=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            port=settings.DATABASE_PORT
        )

    @classmethod
    def execute_query(cls, query, params=None, fetch=False):
        conn = cls.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                if fetch:
                    return cur.fetchall()
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
