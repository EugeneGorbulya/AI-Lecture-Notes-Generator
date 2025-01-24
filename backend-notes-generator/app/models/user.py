import string
import random
from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship

def generate_random_username():
    return "user_" + "".join(random.choices(string.ascii_letters + string.digits, k=8))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False, default=generate_random_username)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    chats = relationship("Chat", back_populates="owner")
