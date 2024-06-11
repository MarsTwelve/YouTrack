from pydantic import BaseModel, Field
from typing import Optional


class VehicleSearch(BaseModel):
    make: str
    model: Optional[str] = Field(default=None)
