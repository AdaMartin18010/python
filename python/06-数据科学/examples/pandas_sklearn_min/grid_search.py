import json

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV


def main() -> None:
    df = pd.DataFrame({
        "x1": [0, 1, 2, 3, 4, 5, 6, 7],
        "x2": [1, 0, 1, 0, 1, 0, 1, 0],
        "y":  [0, 0, 0, 1, 1, 1, 1, 1],
    })
    X = df[["x1", "x2"]]
    y = df["y"]

    model = LogisticRegression(max_iter=500)
    search = GridSearchCV(model, param_grid={
        "C": [0.1, 1.0, 10.0],
        "penalty": ["l2"],
        "solver": ["lbfgs"],
    }, cv=3, scoring="f1")
    search.fit(X, y)

    print(json.dumps({
        "best_params": search.best_params_,
        "best_score": float(search.best_score_),
    }))


if __name__ == "__main__":
    main()


