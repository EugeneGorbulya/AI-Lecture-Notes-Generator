from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: int
    issued_at: int

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
