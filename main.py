from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.session import engine
from db.base import Base
from routes import auth,users
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown logic (optional)
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(users.router)