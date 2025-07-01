from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)  # Text type for long content
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_modified_date = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Relationship to User
    user = relationship("User", back_populates="notes")