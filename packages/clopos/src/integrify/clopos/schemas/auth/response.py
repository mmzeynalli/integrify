from typing import Literal, Optional

from pydantic import BaseModel


class AuthResponse(BaseModel):
    success: Literal[True]
    token: str
    token_type: str
    expires_in: int
    expires_at: Optional[int] = None
    message: Optional[str] = None
