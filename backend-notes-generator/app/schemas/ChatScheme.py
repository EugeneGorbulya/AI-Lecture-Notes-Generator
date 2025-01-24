from app.schemas.BaseScheme import BaseScheme, str_big_factory
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ChatBase(BaseScheme):
    name: str = str_big_factory()


class ChatCreate(ChatBase):
    pass


class ChatResponse(BaseModel):
    id: int
    owner_id: int
    created_at: datetime
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, chat):
        return cls(
            id=chat.id,
            owner_id=chat.owner_id,
            name=chat.name,
            created_at=chat.created_at,
        )
