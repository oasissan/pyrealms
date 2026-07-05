from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .auth import BasicAuthMiddleware
from .database import Base, SessionLocal, engine
from .routers import actions, pages, chatbot
from .seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run simple SQLite migrations to add Gemini cookie columns if they don't exist yet
    from sqlalchemy import text
    for col in ["gemini_session_cookie", "gemini_cookie_ts"]:
        try:
            with engine.begin() as conn:
                conn.execute(text(f"ALTER TABLE settings ADD COLUMN {col} VARCHAR"))
        except Exception:
            pass
            
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title="PyRealms", lifespan=lifespan)
app.add_middleware(BasicAuthMiddleware)
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).resolve().parent / "static"),
    name="static",
)
app.include_router(pages.router)
app.include_router(actions.router)
app.include_router(chatbot.router)

