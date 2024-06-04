from pydantic import BaseModel
from typing import Optional


class UserUpdate(BaseModel):
    user_id: Optional[str] = None
    update_field: str
    update_param: str
