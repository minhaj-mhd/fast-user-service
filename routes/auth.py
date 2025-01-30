from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from db.models import User
from schemas.user import UserCreate, UserResponse
from schemas.token import Token
from jose import jwt, JWTError
from core.security import (
    get_password_hash, 
    create_access_token, 
    oauth2_scheme,
    get_current_user
)
from utils.email import send_verification_email
from utils.redis import publish_event
from datetime import timedelta

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    existing_user = await db.get(User, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    await db.commit()
    
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(hours=1)
    )
    
    background_tasks.add_task(send_verification_email, user.email, token)
    publish_event("user_registered", {"email": user.email})
    
    return UserResponse(email=new_user.email, is_verified=new_user.is_verified)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify/{token}")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        user = await db.get(User, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_verified = True
        await db.commit()
        return {"message": "Email verified successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")