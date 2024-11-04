import sqlite3

import pytest


@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")
    yield connection
    connection.close()
