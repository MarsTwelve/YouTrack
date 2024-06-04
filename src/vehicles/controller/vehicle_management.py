from src.vehicles.services.vehicle_management import VehicleManagementInterface
from src.vehicles.schemas.input import VehicleInput
from src.vehicles.schemas.update import VehicleUpdate
from src.vehicles.schemas.search import VehicleSearch


class VehicleManagementController:
    def __init__(self, client_service: VehicleManagementInterface):
        self.__client_service = client_service

    def create_vehicle(self, vehicle_data: VehicleInput):
        return self.__client_service.create_vehicle(vehicle_data)

    def read_all_vehicles(self, page: int, page_size: int):
        return self.__client_service.read_all_vehicles(page, page_size)

    def find_vehicle_by_name(self, vehicle_data: VehicleSearch):
        return self.__client_service.find_vehicle_by_name(vehicle_data)

    def update_vehicle(self, vehicle_data: VehicleUpdate):
        return self.__client_service.update_vehicle(vehicle_data)

    def delete_vehicle(self, vehicle_id: str):
        return self.__client_service.delete_vehicle(vehicle_id)
