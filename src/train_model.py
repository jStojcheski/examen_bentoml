import bentoml
import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from typing import Tuple


def load_train_data() -> Tuple[pd.DataFrame, pd.Series]:
    X_train = pd.read_csv("./data/processed/X_train.csv")
    assert len(X_train) > 0

    y_train = pd.read_csv("./data/processed/y_train.csv")
    assert len(y_train) > 0

    return X_train, y_train


def load_test_data() -> Tuple[pd.DataFrame, pd.Series]:
    X_test = pd.read_csv("./data/processed/X_test.csv")
    assert len(X_test) > 0

    y_test = pd.read_csv("./data/processed/y_test.csv")
    assert len(y_test) > 0

    return X_test, y_test


if __name__ == "__main__":
    X_train, y_train = load_train_data()

    model = AdaBoostRegressor()
    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    mae_train = mean_absolute_error(y_train, train_predictions)
    print(f"MSE train is: {mae_train:.04f}")
    mse_train = mean_squared_error(y_train, train_predictions)
    print(f"MSE train is: {mse_train:.04f}")

    X_test, y_test = load_test_data()
    test_predictions = model.predict(X_test)
    mae_test = mean_absolute_error(y_test, test_predictions)
    print(f"MAE test is: {mae_test:.04f}")
    mse_test = mean_squared_error(y_test, test_predictions)
    print(f"MSE test is: {mse_test:.04f}")

    bento_model = bentoml.sklearn.save_model("admission_model", model)
    print(f"Model saved: {bento_model}")
