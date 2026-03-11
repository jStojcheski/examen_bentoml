import bentoml
import logging
from starlette import status
from starlette.responses import JSONResponse

from src.auth import authenticate_user, create_access_token
from src.auth import JWTAuthMiddleware
from src.data_types import PredictionInput
from src.prepare_data import normalize_data

logging.basicConfig(level=logging.INFO)


@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)
class MyBentoML:
    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model("admission_model")

    @bentoml.api(route="/login")
    def login(
        self,
        username: str,
        password: str,
    ):
        user = authenticate_user(username, password)

        if user is None:
            err = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Basic"},
                ),
            )
            logging.error(err, exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": str(err),
                },
            )

        access_token = create_access_token(data={"sub": user.name}, is_admin=user.is_admin)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": access_token,
                "token_type": "bearer",
            },
        )

    @bentoml.api(route="/predict")
    def predict(
        self,
        gre_score: int,
        toefl_score: int,
        university_rating: int,
        sop: float,
        lor: float,
        cgpa: float,
        research: int,
    ):
        try:
            input_data = PredictionInput(
                gre_score=gre_score,
                toefl_score=toefl_score,
                university_rating=university_rating,
                sop=sop,
                lor=lor,
                cgpa=cgpa,
                research=research,
            )
            model_input = input_data.to_pandas()
            normalized_model_input = normalize_data(model_input, exclude_target=True)
        except Exception as err:
            logging.error(err, exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": str(err),
                },
            )

        predictions = self.model.predict(normalized_model_input)
        prediction = predictions[0]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=prediction,
        )


MyBentoML.add_asgi_middleware(JWTAuthMiddleware)
