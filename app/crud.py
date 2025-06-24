import uuid
from sqlmodel import Session, select
from app.models import Category
from datetime import datetime
# TODO: write the code for the following CRUD operations
# 4. Get all the categories
# 5. Update a category (takes as input the new "name")

# category_in stands for category input. To create a category we only require a
# single string, which is the category "name" or "description". No need for custom models
def create_category(*, session: Session, category_in: str) -> Category:
    db_obj = Category(category=category_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_category_by_id(*, session: Session, id: uuid.UUID) -> Category | None:
    statement = select(Category).where(Category.id == id)
    session_category = session.exec(statement).first()
    if session_category.deleted_at != None:
        return None
    return session_category

def delete_category_by_id(*, session: Session, id: uuid.UUID) -> bool:
    category = get_category_by_id(session=session, id=id)
    if not category:
        return False
    category.deleted_at = datetime.now()
    category.updated_at = category.deleted_at
    session.add(category)
    session.commit()
    return True