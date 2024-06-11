from abc import ABC, abstractmethod
from src.vehicles.schemas.input import VehicleInput
from src.vehicles.schemas.search import VehicleSearch
from src.vehicles.schemas.update import VehicleUpdate


class VehicleManagementInterface(ABC):

    @abstractmethod
    def create_vehicle(self, vehicle_data: VehicleInput):
        pass

    @abstractmethod
    def read_all_vehicles(self, page: int, page_size: int):
        pass

    @abstractmethod
    def find_vehicle_by_name(self, vehicle_data: VehicleSearch):
        pass

    @abstractmethod
    def update_vehicle(self, vehicle_data: VehicleUpdate):
        pass

    @abstractmethod
    def select_vehicle_by_id(self, vehicle_id: str):
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: str):
        pass
