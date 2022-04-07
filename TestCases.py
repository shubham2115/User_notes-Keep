import pytest
from app import app

def test_registration():
    response = app.test_client().get('/registration')

    assert response.status_code == 200
    # assert response.data.decode('utf-8') == 'Testing, Flask!'