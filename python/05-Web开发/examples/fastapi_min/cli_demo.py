import os
import sys
import time
import requests


BASE = os.environ.get("BASE", "http://127.0.0.1:8000")
API_KEY = os.environ.get("X_API_KEY", os.environ.get("APP_APP_NAME", "fastapi-min"))


def main() -> int:
    print("health:", requests.get(f"{BASE}/health").json())

    r = requests.post(f"{BASE}/items", json={"name": "book", "price": 9.9})
    print("create item:", r.json())

    r = requests.get(f"{BASE}/users", params={"limit": 2, "offset": 0})
    print("users page:", r.json())

    r = requests.get(f"{BASE}/protected", headers={"X-API-Key": API_KEY})
    print("protected:", r.json())

    r = requests.post(f"{BASE}/jobs", params={"seconds": 5, "name": "demo"})
    print("add job:", r.json())

    time.sleep(1)
    r = requests.get(f"{BASE}/jobs")
    print("jobs:", r.json())

    return 0


if __name__ == "__main__":
    sys.exit(main())


