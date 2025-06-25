import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.models import Category, CategoryIn
from app.crud import get_category_by_id, create_category, delete_category_by_id, update_category_by_id, get_all_categories
from app.db import engine
from typing import Annotated, List


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

@router.post("/", status_code=201)
# TODO: detect when the user tries to create a category that already "exists" (like a sports category
# that was soft-deleted) and undo that soft-delete
# It seems to me that this situation produces a sqlalchemy.exc.IntegrityError and it should be the only one possible
def post_category(session: SessionDep, category: CategoryIn) -> Category | None:
    created_category = create_category(session=session, category_in=category.category)
    return created_category
    
@router.delete("/{id}", status_code=204)
def delete_category(session: SessionDep, id: uuid.UUID) -> None:
    found = delete_category_by_id(session=session, id=id)
    if not found:
        raise HTTPException(status_code=404, detail="Category not found")
    
@router.put("/{id}")
def update_category(session: SessionDep, id: uuid.UUID, category: CategoryIn) -> Category | None:
    updated_category = update_category_by_id(session=session, id=id, new_name=category.category)
    if updated_category == None:
        raise HTTPException(status_code=404, details="Category not found")
    return updated_category

@router.get("/")
def read_all_categories(session: SessionDep) -> List[Category]:
    categories = get_all_categories(session=session)
    return list(categories)