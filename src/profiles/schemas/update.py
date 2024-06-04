from pydantic import BaseModel


class ProfileUpdate(BaseModel):
    profile_id: str
    update_field: str
    update_param: str
