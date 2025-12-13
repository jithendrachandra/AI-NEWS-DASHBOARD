from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db import crud
from pydantic import BaseModel

class SourceCreate(BaseModel):
    name: str
    url: str

router = APIRouter()

@router.post("/")
def add_source(source: SourceCreate, db: Session = Depends(get_db)):
    return crud.create_source(db, source.name, source.url)

@router.get("/")
def list_sources(db: Session = Depends(get_db)):
    return crud.get_active_sources(db)