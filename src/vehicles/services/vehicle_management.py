from abc import ABC

from src.vehicles.interfaces.i_vehicle_service import VehicleManagementInterface
from src.vehicles.interfaces.i_vehicle_repository import VehicleRepositoryInterface
from src.vehicles.schemas.input import VehicleInput
from src.vehicles.schemas.search import VehicleSearch
from src.vehicles.schemas.update import VehicleUpdate


class VehicleManagementService(VehicleManagementInterface, ABC):
    def __init__(self, repository: VehicleRepositoryInterface):
        self.__repository = repository

    def create_vehicle(self, vehicle_data: VehicleInput):
        return self.__repository.insert_new_vehicle(vehicle_data)

    def read_all_vehicles(self, page: int, page_size: int):
        return self.__repository.select_all_vehicles(page, page_size)

    def find_vehicle_by_name(self, vehicle_data: VehicleSearch):
        return self.__repository.select_vehicle_by_search_criteria(vehicle_data)

    def update_vehicle(self, vehicle_data: VehicleUpdate):
        return self.__repository.update_vehicle_info(vehicle_data)

    def select_vehicle_by_id(self, vehicle_id: str):
        return self.__repository.select_vehicle_by_id(vehicle_id)

    def delete_vehicle(self, vehicle_id: str):
        return self.__repository.delete_vehicle(vehicle_id)
