import requests
from starlette import status


def test_api_returns_valid_jwt_token_for_correct_credentials():
    response = requests.post(
        "http://localhost:3000/login",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "username": "admin",
            "password": "secret123",
        },
    )
    assert response.status_code == status.HTTP_200_OK


def test_api_returns_401_error_for_incorrect_credentials():
    response = requests.post(
        "http://localhost:3000/login",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "username": "bad_user",
            "password": "worse_password",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
