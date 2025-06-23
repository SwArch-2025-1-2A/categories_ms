from sqlmodel import SQLModel, create_engine
from os import getenv

DATABASE_URL = str(getenv("DATABASE_URL"))
engine = create_engine(DATABASE_URL, echo=True)

def init_db() -> None:
    # This is based on a FastAPI template in GitHub from the FastAPI creator
    # He recommends running migrations using Alembic, but our schema and backend
    # is so simple that I don't consider that necessary
    from app.models import Category
    SQLModel.metadata.create_all(engine)