import argparse
import json
from pathlib import Path

import joblib
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Load model.joblib and predict")
    parser.add_argument("--x1", type=float, required=True)
    parser.add_argument("--x2", type=float, required=True)
    parser.add_argument("--model", type=Path, default=Path("model.joblib"))
    args = parser.parse_args()

    model = joblib.load(args.model)
    X = pd.DataFrame({"x1": [args.x1], "x2": [args.x2]})
    y_pred = model.predict(X)
    print(json.dumps({"prediction": int(y_pred[0])}))


if __name__ == "__main__":
    main()


