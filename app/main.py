from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.base import Base
from app.db.session import engine
from app.api import auth, note
from app.models import user  # Import models here


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(title="Notepad API", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(note.router, prefix="/notes", tags=["Notes"])

@app.get("/")
async def read_root():
    return {"message": "Notepad API is running!"}