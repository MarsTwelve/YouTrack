from pydantic import BaseModel
from typing import Optional


class VehicleSearch(BaseModel):
    make: str
    model: Optional[str]
