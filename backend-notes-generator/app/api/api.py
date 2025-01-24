from fastapi import APIRouter
from app.api.routes.user import router as user_router
from app.api.routes.chat import router as chat_router
from app.api.routes.message import router as message_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(chat_router, prefix="/chats", tags=["chats"])
api_router.include_router(message_router, prefix="/message", tags=["message"])