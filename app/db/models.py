from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID


class ShortURL(SQLModel, table=True):
    __tablename__ = "short_urls"

    id: UUID = Field(primary_key=True)
    original_url: str = Field(index=True, max_length=2048)
    short_code: str = Field(unique=True, index=True, max_length=22)
    visit_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
