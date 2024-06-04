from pydantic import BaseModel
from typing import Optional


class VehicleInput(BaseModel):
    vehicle_make: str
    vehicle_model: str
    vehicle_trim: Optional[str] | None
    vehicle_color: str
    manufacture_year: int
    number_plate: str
    client_id: str
