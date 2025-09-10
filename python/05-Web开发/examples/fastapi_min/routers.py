from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"pong": "ok"}


