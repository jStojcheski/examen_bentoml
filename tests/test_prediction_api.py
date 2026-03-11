import requests
from starlette import status


VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTc3MzE1MDgwM30.At-Nn2_alTQE-V6eSDqwlGnDibBc5oVw0pf5HkVhkME"

VALID_GRE_SCORE = 327
VALID_TOEFL_SCORE = 113
VALID_UNIVERSITY_RATING = 4
VALID_SOP_VALUE = 4.5
VALID_LOR_VALUE = 4.5
VALID_CGPA_VALUE = 9.04
VALID_RESEARCH_VALUE = 0


def get_data(
    gre_score: int = VALID_GRE_SCORE,
    toefl_score: int = VALID_TOEFL_SCORE,
    university_rating: int = VALID_UNIVERSITY_RATING,
    sop: float = VALID_SOP_VALUE,
    lor: float = VALID_LOR_VALUE,
    cgpa: float = VALID_CGPA_VALUE,
    research: int = VALID_RESEARCH_VALUE,
):
    return dict(
        gre_score=gre_score,
        toefl_score=toefl_score,
        university_rating=university_rating,
        sop=sop,
        lor=lor,
        cgpa=cgpa,
        research=research,
    )


def test_api_return_401_error_if_jwt_token_is_missing():
    data = get_data()
    response = requests.post(
        "http://localhost:3000/predict",
        data=data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_api_return_401_error_if_jwt_token_is_invalid():
    data = get_data()
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": "Bearer INVALID_TOKEN",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_api_returns_valid_prediction_for_correct_input_data():
    data = get_data()
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK


def test_api_returns_error_for_invalid_gre_score():
    data = get_data(gre_score=-100)
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_api_returns_error_for_invalid_toefl_score():
    data = get_data(toefl_score=-100)
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_api_returns_error_for_invalid_university_ranking_value():
    data = get_data(university_rating=-100)
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_api_returns_error_for_invalid_sop_value():
    data = get_data(sop=-100)
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_api_returns_error_for_invalid_lor_value():
    data = get_data(lor=-100)
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_api_returns_error_for_invalid_cgpa_value():
    data = get_data(cgpa=-100)
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_api_returns_error_for_invalid_research_value():
    data = get_data(research=-100)
    response = requests.post(
        "http://localhost:3000/predict",
        headers={
            "Authorization": f"Bearer {VALID_TOKEN}",
        },
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
