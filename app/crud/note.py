from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.note import Note
from app.schemas.note_schema import NoteCreate, NoteUpdate


def get_user_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Note]:
    return (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .order_by(Note.created_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_note_by_id(db: Session, note_id: int, user_id: int) -> Optional[Note]:
    return (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id)
        .first()
    )


def create_note(db: Session, note_in: NoteCreate, user_id: int) -> Note:
    note = Note(
        name=note_in.name,
        content=note_in.content,
        user_id=user_id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note_id: int, note_in: NoteUpdate, user_id: int) -> Optional[Note]:
    note = get_note_by_id(db, note_id, user_id)
    if not note:
        return None

    note.name = note_in.name
    note.content = note_in.content
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int, user_id: int) -> bool:
    note = get_note_by_id(db, note_id, user_id)
    if not note:
        return False

    db.delete(note)
    db.commit()
    return True


def get_note_word_count(content: str) -> int:
    return len(content.split())