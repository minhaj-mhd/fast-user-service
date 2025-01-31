from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from db.session import get_db  # Database session
from db.models import User  # User model
from schemas.user import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[str])
async def get_all_users(db: AsyncSession  = Depends(get_db)):
    try:
        # Query all users from the database
        result = await db.execute(select(User.email))
        emails = result.scalars().all()
        # Return the list of users
        return emails
    except Exception as e:
        # Handle any errors
        raise HTTPException(status_code=500, detail=str(e))