from pydantic import BaseModel
from typing import Optional


class VehicleOutput(BaseModel):
    vehicle_id: str
    client_id: str
    profile_id: Optional[str] | None
    vehicle_make: str
    vehicle_model: str
    vehicle_trim: Optional[str] | None
    vehicle_color: str
    manufacture_year: int
    number_plate: str
