from pydantic import BaseModel, Field


class ClientUpdate(BaseModel):
    client_id: str
    update_field: str
    update_param: str
