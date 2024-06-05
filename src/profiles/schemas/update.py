from pydantic import BaseModel
from typing import Union


class ProfileUpdate(BaseModel):
    profile_id: str
    update_field: str
    update_param: Union[str, bool]
