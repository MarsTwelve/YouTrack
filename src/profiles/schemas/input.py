from pydantic import BaseModel, Field


class ProfileInput(BaseModel):
    profile_name: str
    administrator: bool = Field(default=False)
    fuel_avg: bool = Field(default=False)
    speed_avg: bool = Field(default=False)
    route: bool = Field(default=False)
    perimeters: bool = Field(default=False)
    tracking: bool = Field(default=False)
    weather: bool = Field(default=False)
