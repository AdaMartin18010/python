from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .routers import router as v1_router
from .db import init_db, get_session, User

app = FastAPI()


class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)


class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)


@app.on_event("startup")
async def _on_startup() -> None:
    await init_db()


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/items")
def create_item(item: Item) -> dict[str, object]:
    if item.price == 0:
        raise HTTPException(status_code=400, detail="price must be > 0")
    return {"ok": True, "item": item.model_dump()}


@app.post("/users", status_code=201)
async def create_user(payload: UserIn, session: AsyncSession = Depends(get_session)) -> dict[str, object]:
    user = User(name=payload.name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"id": user.id, "name": user.name}


@app.get("/users")
async def list_users(session: AsyncSession = Depends(get_session)) -> list[dict[str, object]]:
    result = await session.execute(select(User))
    return [{"id": u.id, "name": u.name} for u in result.scalars().all()]


# 路由分组
app.include_router(v1_router)
