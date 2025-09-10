import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib


def main() -> None:
    df = pd.DataFrame({
        "x1": [0, 1, 2, 3, 4, 5],
        "x2": [1, 0, 1, 0, 1, 0],
        "y":  [0, 0, 0, 1, 1, 1],
    })
    X = df[["x1", "x2"]]
    y = df["y"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)
    prec = precision_score(y_test, pred, zero_division=0)
    rec = recall_score(y_test, pred, zero_division=0)
    f1 = f1_score(y_test, pred, zero_division=0)

    print({
        "accuracy": round(float(acc), 3),
        "precision": round(float(prec), 3),
        "recall": round(float(rec), 3),
        "f1": round(float(f1), 3),
    })

    # 保存模型
    joblib.dump(model, "model.joblib")


if __name__ == "__main__":
    main()
