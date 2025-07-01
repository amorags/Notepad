from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db  # Adjust import path as needed
from app.schemas.note_schema import NoteCreate, NoteUpdate, NoteOut
from app.crud import note as note_crud # Assuming your CRUD functions are in this module
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[NoteOut])
async def get_notes(
    skip: int = Query(0, ge=0, description="Number of notes to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of notes to return"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve notes for the authenticated user with pagination.
    """
    notes = note_crud.get_user_notes(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit
    )
    return notes

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve a specific note by ID for the authenticated user.
    """
    note = note_crud.get_note_by_id(
        db=db, 
        note_id=note_id, 
        user_id=current_user.id
    )
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new note for the authenticated user.
    """
    note = note_crud.create_note(
        db=db, 
        note_in=note_in, 
        user_id=current_user.id
    )
    return note

@router.put("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update an existing note for the authenticated user.
    """
    note = note_crud.update_note(
        db=db, 
        note_id=note_id, 
        note_in=note_in, 
        user_id=current_user.id
    )
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a note for the authenticated user.
    """
    success = note_crud.delete_note(
        db=db, 
        note_id=note_id, 
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

@router.get("/{note_id}/word-count")
async def get_note_word_count(
    note_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get the word count for a specific note.
    """
    note = note_crud.get_note_by_id(
        db=db, 
        note_id=note_id, 
        user_id=current_user.id
    )
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    word_count = note_crud.get_note_word_count(note.content)
    return {"note_id": note_id, "word_count": word_count}