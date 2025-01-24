from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Message, Chat, User
from app.schemas import MessageCreate, MessageResponse
from app.core.database import get_db
from app.api.deps import get_current_user
from typing import List
from sqlalchemy.future import select
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRASH_DIR = os.path.join(BASE_DIR, "Trash")

os.makedirs(TRASH_DIR, exist_ok=True)

@router.get("/static/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(TRASH_DIR, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )

@router.post("/{chat_id}/file", response_model=MessageResponse)
async def upload_file(
    chat_id: int,
    file: UploadFile,
    type: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    chat = await db.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    file_location = os.path.join(TRASH_DIR, file.filename)

    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())

        file_name = os.path.basename(file_location)

        new_message = Message(
            type=type,
            content=file_name,
            url=file_name,
            chat_id=chat_id,
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        return new_message

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


@router.post("/{chat_id}/", response_model=MessageResponse)
async def create_message(
    chat_id: int,
    message: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    chat = await db.get(Chat, chat_id)
    if not chat or chat.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    new_message = Message(**message.dict())
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message


@router.get("/{chat_id}/", response_model=List[MessageResponse])
async def list_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    chat = await db.get(Chat, chat_id)
    if not chat or chat.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(select(Message).filter(Message.chat_id == chat_id))
    messages = result.scalars().all()
    return [MessageResponse.from_orm(message) for message in messages]
