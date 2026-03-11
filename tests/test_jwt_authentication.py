from starlette import status
import requests


TEST_URL = "http://localhost:3000/predict"
EXPIRED_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MCwiaWF0IjoxNzczMTUwOTMyfQ.vN_bVqqQebtj35gL2EmLeDqyLGkfQG13E2v0dSrfolk"
VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTc3MzE1MDgwM30.At-Nn2_alTQE-V6eSDqwlGnDibBc5oVw0pf5HkVhkME"

TEST_DATA = {
    "gre_score": 327,
    "toefl_score": 113,
    "university_rating": 4,
    "sop": 4.5,
    "lor": 4.5,
    "cgpa": 9.04,
    "research": 0,
}


def test_authentication_fails_if_jwt_token_is_missing():
    response = requests.post(
        url=TEST_URL,
        data=TEST_DATA,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authentication_fails_if_jwt_token_is_invalid():
    response = requests.post(
        url=TEST_URL,
        data=TEST_DATA,
        headers={
            "Authorization": "Bearer INVALID_TOKEN",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authentication_fails_if_jwt_token_has_expired():
    response = requests.post(
        url=TEST_URL,
        data=TEST_DATA,
        headers={
            "Authorization": f"Bearer {EXPIRED_TOKEN}",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token has expired"


def test_authentication_succeeds_with_valid_jwt_token():
    response = requests.post(
        url=TEST_URL,
        data=TEST_DATA,
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
    )
    assert response.status_code == status.HTTP_200_OK
