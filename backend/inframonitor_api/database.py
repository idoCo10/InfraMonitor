import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://inframonitor:inframonitor@127.0.0.1:5432/inframonitor",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

def check_database():
    """Check that the backend can connect to PostgreSQL."""

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        return result.scalar() == 1