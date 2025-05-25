from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models import Chat, Message, User
from app.schemas import ChatResponse, MessageResponse
from app.core.database import get_db
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def create_chat(user_id: int, name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    chat = Chat(owner_id=user_id, name=name)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)

    return ChatResponse.from_orm(chat)

@router.get("/", response_model=List[ChatResponse])
async def list_chats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Chat).filter(Chat.owner_id == current_user.id))
    chats = result.scalars().all()
    return [ChatResponse.from_orm(chat) for chat in chats]