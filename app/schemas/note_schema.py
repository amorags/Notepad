from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class NoteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Note name")
    content: str = Field(..., min_length=10, max_length=10000, description="Note content")

    @validator('content')
    def validate_word_count(cls, v):
        word_count = len(v.split())
        if word_count < 10:  # Assuming minimum 10 words for 10+ word requirement
            raise ValueError('Content must contain at least 10 words')
        return v

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteInDB(NoteBase):
    id: int
    created_date: datetime
    last_modified_date: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True

class NoteOut(NoteInDB):
    pass

class NoteListItem(BaseModel):
    id: int
    name: str
    created_date: datetime
    last_modified_date: Optional[datetime] = None
    word_count: int

    class Config:
        from_attributes = True