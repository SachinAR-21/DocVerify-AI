from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (makes sure all tables are registered)
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routers import health
from app.seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    # simple approach for now: create missing tables on startup
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
