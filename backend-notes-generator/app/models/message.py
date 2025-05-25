from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class MessageType(enum.Enum):
    TEXT = "TEXT"
    VIDEO = "VIDEO"
    FILE = "FILE"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(MessageType), nullable=False)
    content = Column(String, nullable=False)
    url = Column(String, nullable=True)
    previous_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender = Column(String, nullable=False, default="user")
    chat = relationship("Chat", back_populates="messages")

    previous_message = relationship("Message", remote_side=[id])

    class Config:
        from_attributes = True

