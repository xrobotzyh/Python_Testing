from datetime import datetime
from unittest.mock import Mock

import pytest

from server import loadClubs, loadCompetitions, app


def test_loadClubs():
    # setup
    file_loadclubs = loadClubs()
    # Action
    expected_value = 3
    # assert
    assert len(file_loadclubs) == expected_value


def test_loadCompetitions():
    file = loadCompetitions()

    expected_value = 2

    assert len(file) == expected_value


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_showSummary_with_validate_email(client):
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert b'Welcome' in response.data
    assert response.status_code == 200


def test_showSummary_with_unvalidate_email(client):
    response = client.post('/showSummary', data={'email': '11@irontemple.com'})
    assert b'The email is not found' in response.data
    assert response.status_code == 401



