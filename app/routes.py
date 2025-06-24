import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.models import Category
from app.crud import get_category_by_id, create_category, delete_category_by_id
from app.db import engine
from typing import Annotated


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter(prefix="/api/categories")

@router.get("/{id}")
def read_category(session: SessionDep, id: uuid.UUID) -> Category | None :
    category = get_category_by_id(session=session, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/")
def post_category(session: SessionDep, category_name: str) -> Category | None:
    category = create_category(session=session, category_in=category_name)
    return category
    
@router.delete("/{id}")
def delete_category(session: SessionDep, id: uuid.UUID) -> None:
    found = delete_category_by_id(session=session, id=id)
    if not found:
        raise HTTPException(status_code=404, detail="Category not found")