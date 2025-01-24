from pydantic import BaseModel
from typing import Optional
from app.models.message import MessageType

class MessageCreate(BaseModel):
    type: MessageType
    content: str
    url: Optional[str] = None
    previous_message_id: Optional[int] = None
    chat_id: int

class MessageResponse(BaseModel):
    id: int
    type: MessageType
    content: str
    url: Optional[str] = None
    previous_message_id: Optional[int] = None
    chat_id: int

    class Config:
        from_attributes = True
