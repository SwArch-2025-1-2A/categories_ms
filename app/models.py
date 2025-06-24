import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

# TODO: datetimes should have a timezone
class Category(SQLModel, table=True):
    # I assume that a primary key is automatically an index, not nullable and unique
    # Hopefully it does work that way
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category: str = Field(max_length=50, nullable=False, unique=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    # Another valid approach would be to use the type Optional[datetime], but it seems to me that
    # datetime | None is more widely used
    deleted_at: datetime | None = Field(default=None, nullable=True)