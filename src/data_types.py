import pandas as pd
from pydantic import BaseModel
from typing import Any, Dict, List


class PredictionInput(BaseModel):
    gre_score: int
    toefl_score: int
    university_rating: int
    sop: float
    lor: float
    cgpa: float
    research: int

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

        assert 0 <= self.gre_score <= 340
        assert 0 <= self.toefl_score <= 120
        assert 0 <= self.university_rating <= 5
        assert 0 <= self.sop <= 5
        assert 0 <= self.lor <= 5
        assert 0 <= self.cgpa <= 10
        assert self.research in {0, 1}

    def to_data_point(self) -> Dict[str, Any]:
        return {
            "GRE Score": self.gre_score,
            "TOEFL Score": self.toefl_score,
            "University Rating": self.university_rating,
            "SOP": self.sop,
            "LOR ": self.lor,
            "CGPA": self.cgpa,
            "Research": self.research,
        }

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame([self.to_data_point()])


class User(BaseModel):
    name: str
    password: str
    is_admin: bool


def load_users_db() -> List[User]:
    user_df = pd.read_csv("data/users.csv")

    users: List[User] = []
    for i in user_df.index:
        user_item = user_df.iloc[i]
        user = User(
            name=user_item["name"],
            password=user_item["password"],
            is_admin=user_item["is_admin"],
        )
        users.append(user)

    return users
