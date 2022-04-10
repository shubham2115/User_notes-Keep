import json

import pytest
from app import app
from flask import session

def test_access_session(client):
    with client:
        client.post("/auth/login", data={"username": "Mohit"})
        # session is still accessible
        assert session["user_id"] == 31

# data_ = {
#     "user_name": "Shubham",
#     "name": "abced",
#     "email": "s.shrikhande1@gmail.com",
#     "password1": "12345",
#     "password2": "12345"
# }
# data = json.dumps(data_)
#
#
# def test_registration():
#     response = app.test_client().post("http://127.0.0.1:130/registration", data=data_)
#     content_type = 'application/json'
#     assert response.status_code == 200
#     # assert response.data.decode('utf-8') == 'Testing, Flask!'
#
# # def test_user_registration_when_given_valid_payload(self):
# #     response = self.client.post(reverse('registration'),data=json.dumps(self.valid_payload),
# #                                      content_type = 'application/json'
# #     self.assertEquals(response.status_code, status.HTTP_201_CREATED)
