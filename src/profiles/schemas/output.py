from pydantic import BaseModel, Field


class ProfileOutput(BaseModel):
    profile_id: str
    vehicle_id_list: list[str]
    profile_name: str
    administrator: bool = Field(default=False)
    fuel_avg: bool = Field(default=False)
    speed_avg: bool = Field(default=False)
    route: bool = Field(default=False)
    perimeters: bool = Field(default=False)
    tracking: bool = Field(default=False)
    weather: bool = Field(default=False)
