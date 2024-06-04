from pydantic import BaseModel, Field
from typing import Optional


class UserOutput(BaseModel):
    user_id: str
    username: str
    email: str
    user_profile_id: Optional[str] = None


class UserOptions(BaseModel):
    language: str = Field(default="Portuguese")
    currency: str = Field(default="BRL")
    country: str = Field(default="Brazil")
    unit_speed: str = Field(default="KMH")
    unit_volume: str = Field(default="Liter")
    unit_length: str = Field(default="Kilometer")
    unit_temp: str = Field(default="Celsius")
