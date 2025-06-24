import uuid
from sqlmodel import Session, select
from app.models import Category
# TODO: write the code for the following CRUD operations
# 1. Create a new category (takes the "name" as input)
# 2. Soft-delete a category
# 3. Get a category by UUID
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
    return session_category