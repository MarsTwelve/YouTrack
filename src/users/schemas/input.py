from pydantic import BaseModel, Field


class UserInput(BaseModel):
    username: str
    password: str
    email: str
    language: str = Field(default="Portuguese")
    currency: str = Field(default="BRL")
    country: str = Field(default="Brazil")
    unit_speed: str = Field(default="KMH")
    unit_volume: str = Field(default="Liter")
    unit_length: str = Field(default="Kilometer")
    unit_temp: str = Field(default="Celsius")
    client_id: str
