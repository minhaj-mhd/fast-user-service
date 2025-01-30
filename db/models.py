from sqlalchemy import Column, String, Boolean
from .base import Base

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)