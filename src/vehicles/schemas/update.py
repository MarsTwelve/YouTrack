from pydantic import BaseModel


class VehicleUpdate(BaseModel):
    vehicle_id: str
    update_field: str
    update_param: str
