import pytest

from src.clients.schemas.input import ClientInput
from src.users.schemas.input import UserInput
from src.vehicles.schemas.input import VehicleInput


@pytest.fixture()
def make_client_schema():
    def make(name: str = "Standard Name",
             company_name: str = "Standard Company Name",
             cellphone: str = "+55 (14)991031566",
             cpf_cnpj: str = "464.085.468-46"):
        clients_schema = ClientInput(name=name,
                                     company_name=company_name,
                                     cellphone=cellphone,
                                     cpf_cnpj=cpf_cnpj, )
        return clients_schema

    return make


@pytest.fixture()
def make_user_schema():
    def make(username: str = "Standard Username",
             password: str = "P4ssW0rd_",
             email: str = "standard.std@email.provider.com",
             language: str = "Portuguese",
             currency: str = "BRL",
             country: str = "Brazil",
             unit_speed: str = "KMH",
             unit_volume: str = "Liter",
             unit_length: str = "Kilometer",
             unit_temp: str = "Celsius",
             client_id: str = "30350b587b11479f91a0a7caabcfe328"):
        user_schema = UserInput(username=username,
                                password=password,
                                email=email,
                                language=language,
                                currency=currency,
                                country=country,
                                unit_speed=unit_speed,
                                unit_volume=unit_volume,
                                unit_length=unit_length,
                                unit_temp=unit_temp,
                                client_id=client_id)
        return user_schema

    return make


@pytest.fixture()
def make_vehicle_schema():
    def make(vehicle_make: str = "Standard Vehicle Brand",
             vehicle_model: str = "Standard Vehicle Model",
             vehicle_trim: str | None = "Standard Vehicle Trim",
             vehicle_color: str = "Standard Vehicle Color",
             manufacture_year: str = 2024,
             number_plate: str = "AWS3F98",
             client_id: str = "30350b587b11479f91a0a7caabcfe328"):
        vehicle_schema = VehicleInput(vehicle_make=vehicle_make,
                                      vehicle_model=vehicle_model,
                                      vehicle_trim=vehicle_trim,
                                      vehicle_color=vehicle_color,
                                      manufacture_year=manufacture_year,
                                      number_plate=number_plate,
                                      client_id=client_id)

        return vehicle_schema

    return make
