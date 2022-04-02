import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "Saeed12#$")
    user, db_name = "saeed", "DataRepository"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_sqlite_uri():
    return "sqlite:///data/data.db"


