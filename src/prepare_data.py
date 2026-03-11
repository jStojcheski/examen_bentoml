import pandas as pd
from sklearn.model_selection import train_test_split
from typing import Tuple

NORMALIZERS = {
    "GRE Score": 340,
    "TOEFL Score": 120,
    "University Rating": 5,
    "SOP": 5,
    "LOR ": 5,
    "CGPA": 10,
    "Research": 1,
    "Chance of Admit ": 1,
}

TARGET = "Chance of Admit "


def read_raw_data() -> pd.DataFrame:
    df = pd.read_csv("./data/raw/admission.csv", index_col="Serial No.")
    return df


def normalize_data(df: pd.DataFrame, exclude_target: bool = False) -> pd.DataFrame:
    normalizers = NORMALIZERS if not exclude_target else {k: v for k, v in NORMALIZERS.items() if k != TARGET}
    normalized_data = df / normalizers
    assert (0 <= normalized_data).all().all() and (normalized_data <= 1).all().all()
    return normalized_data


def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    train_df, test_df = train_test_split(df, train_size=0.8, random_state=0)

    X_train = train_df.drop(TARGET, axis=1)
    y_train = train_df[TARGET]

    X_test = test_df.drop(TARGET, axis=1)
    y_test = test_df[TARGET]

    return X_train, y_train, X_test, y_test


def prepare_data() -> None:
    df = read_raw_data()
    normalized_data = normalize_data(df)
    X_train, y_train, X_test, y_test = split_data(normalized_data)

    X_train.to_csv("./data/processed/X_train.csv", index=False)
    y_train.to_csv("./data/processed/y_train.csv", index=False)
    X_test.to_csv("./data/processed/X_test.csv", index=False)
    y_test.to_csv("./data/processed/y_test.csv", index=False)


if __name__ == "__main__":
    prepare_data()
