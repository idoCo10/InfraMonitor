import os

import pytest
from sqlalchemy import text

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://"
    "inframonitor:inframonitor@127.0.0.1:5432/inframonitor_test"
)


@pytest.fixture(autouse=True)
def clean_test_database():
    from inframonitor_api.database import engine

    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE reports, hosts RESTART IDENTITY CASCADE")
        )

    yield