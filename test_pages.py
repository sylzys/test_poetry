import pytest
from flask import current_app

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():  # New!!
            assert current_app.config["ENV"] == "production"
        yield client


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Churn prediction" in response.data
