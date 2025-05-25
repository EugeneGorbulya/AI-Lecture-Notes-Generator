import os
import logging
import asyncio
from typing import List
from pathlib import Path
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    Form,
    BackgroundTasks,
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Message, Chat, User
from app.schemas import MessageCreate, MessageResponse
from app.core.database import get_db
from app.api.deps import get_current_user
from app.functions.process_pipeline import process_video_to_tex

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_DIR = os.path.join(BASE_DIR, "files")
os.makedirs(FILES_DIR, exist_ok=True)


@router.get("/static/{file_name}")
async def download_file(file_name: str):
    if file_name.endswith(".tex"):
        file_path = os.path.join(FILES_DIR, "tex", file_name)
    else:
        file_path = os.path.join(FILES_DIR, file_name)

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

    file_location = os.path.join(FILES_DIR, file.filename)

    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())

        file_name = os.path.basename(file_location)
        is_video = file.filename.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))

        new_message = Message(
            type=type,
            content=file_name,
            url=file_name,
            chat_id=chat_id,
            sender="user",
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)

        if is_video:
            asyncio.create_task(handle_video_processing(file_location, chat_id, new_message.id))

        return new_message

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


async def handle_video_processing(file_path: str, chat_id: int, user_message_id: int):
    from app.core.session import async_session
    from app.models import Message
    from app.functions.process_pipeline import process_video_to_tex
    import os
    import logging

    async with async_session() as session:
        try:
            tex_path = process_video_to_tex(file_path, FILES_DIR)
            tex_file_name = os.path.basename(tex_path)

            bot_message = Message(
                type="FILE",
                content=tex_file_name,
                url=f"tex/{tex_file_name}",
                chat_id=chat_id,
                sender="bot",
                previous_message_id=user_message_id,
            )
            session.add(bot_message)
            await session.commit()

        except Exception as e:
            logging.error(f"[handle_video_processing] Ошибка обработки видео: {e}")




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

    new_message = Message(
        **message.dict(),
        sender="user",
    )
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

    result = await db.execute(select(Message).filter(Message.chat_id == chat_id).order_by(Message.id))
    messages = result.scalars().all()
    return [MessageResponse.from_orm(message) for message in messages]