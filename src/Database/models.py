from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from typing import Optional, List
from uuid import uuid4


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex, unique=True)
    pass


class ClientModel(Base):
    __tablename__ = "clients_table"

    name: Mapped[str] = mapped_column(String(254))
    company_name: Mapped[str] = mapped_column(String(255))
    cellphone: Mapped[str] = mapped_column(String(17))
    cpf_cnpj: Mapped[str] = mapped_column(String(18))
    user: Mapped[List["UserModel"]] = relationship(back_populates="client")


class UserModel(Base):
    __tablename__ = "users_table"

    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(254))
    language: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    country: Mapped[str] = mapped_column(String(16))
    unit_length: Mapped[str] = mapped_column(String(32))
    unit_speed: Mapped[str] = mapped_column(String(32))
    unit_volume: Mapped[str] = mapped_column(String(32))
    unit_temp: Mapped[str] = mapped_column(String(32))

    client_id: Mapped[str] = mapped_column(ForeignKey("clients_table.id"))
    client: Mapped["ClientModel"] = relationship(back_populates="user")

    profile_id: Mapped[Optional[str]] = mapped_column(String(32), ForeignKey("profiles_table.id"))
    profile: Mapped[Optional["ProfileModel"]] = relationship(back_populates="user")


profiles_vehicles_model = Table(
    "profiles_vehicles",
    Base.metadata,
    Column("profile_id", String(32), ForeignKey("profiles_table.id"), primary_key=True),
    Column("vehicle_id", String(32), ForeignKey("vehicles_table.id"), primary_key=True)
)


class ProfileModel(Base):
    __tablename__ = "profiles_table"

    profile_name: Mapped[str] = mapped_column(String(255))
    administrator: Mapped[bool] = mapped_column(Boolean)
    fuel_avg: Mapped[bool] = mapped_column(Boolean)
    speed_avg: Mapped[bool] = mapped_column(Boolean)
    route: Mapped[bool] = mapped_column(Boolean)
    perimeters: Mapped[bool] = mapped_column(Boolean)
    tracking: Mapped[bool] = mapped_column(Boolean)
    weather: Mapped[bool] = mapped_column(Boolean)

    user: Mapped[List["UserModel"]] = relationship(back_populates="profile")

    vehicles: Mapped[List["VehicleModel"]] = relationship(secondary=profiles_vehicles_model, back_populates="users")


class VehicleModel(Base):
    __tablename__ = "vehicles_table"

    vehicle_make: Mapped[str] = mapped_column(String(16))
    vehicle_model: Mapped[str] = mapped_column(String(16))
    vehicle_trim: Mapped[Optional[str]] = mapped_column(String(16))
    vehicle_color: Mapped[str] = mapped_column(String(16))
    model_year: Mapped[str] = mapped_column(String(4))
    number_plate: Mapped[str] = mapped_column(String(7))

    client_id: Mapped[str] = mapped_column(String(32), ForeignKey("clients_table.id"))
    users: Mapped[List["ProfileModel"]] = relationship(secondary=profiles_vehicles_model, back_populates="vehicles")
