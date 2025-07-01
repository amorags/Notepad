from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base  # use the same Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")