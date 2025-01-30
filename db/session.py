from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Create an async database engine
engine = create_async_engine(
    settings.DATABASE_URL,  # Use the DATABASE_URL from settings
    echo=True,  # Log SQL queries (useful for debugging)
    future=True  # Enable SQLAlchemy 2.0 behavior
)

# Create a session factory for async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent attributes from expiring after commit
    autoflush=False  # Disable autoflush for better control
)

# Dependency to get an async database session
async def get_db():
    """
    Provides an async database session for dependency injection.
    Automatically closes the session after the request is complete.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()