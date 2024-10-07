import os

from dotenv import load_dotenv
load_dotenv()


class PostgresConfig:
    host = os.environ.get("POSTGRES_HOST")
    port = int(os.environ.get("POSTGRES_PORT"))
    db_name = os.environ.get("POSTGRES_DB_NAME")
    username = os.environ.get("POSTGRES_USERNAME")
    password = os.environ.get("POSTGRES_PASSWORD")
    pool_size = int(os.environ.get("POSTGRES_POOL_SIZE"))
    max_overflow = int(os.environ.get("POSTGRES_MAX_OVERFLOW"))


class ServerConfig:
    host = os.environ.get("APP_HOST")
    port = int(os.environ.get("APP_PORT"))
    release = os.environ.get("APP_RELEASE")
    name = os.environ.get("APP_NAME")
    sentry_dsn = os.environ.get("SENTRY_DSN")
    logging_level = int(os.environ.get("LOGGING_LEVEL"))
    logging_format = (
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
