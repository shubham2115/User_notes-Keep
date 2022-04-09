import json

import pytest
from app import app

data_ = {
    "user_name": "Shubham",
    "name": "abced",
    "email": "s.shrikhande1@gmail.com",
    "password1": "12345",
    "password2": "12345"
}
data = json.dumps(data_)


def test_registration():
    response = app.test_client().post('/registration', data=data_)

    assert response.status_code == 200
    # assert response.data.decode('utf-8') == 'Testing, Flask!'
