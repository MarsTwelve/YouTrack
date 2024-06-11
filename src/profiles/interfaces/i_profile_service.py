from abc import ABC, abstractmethod

from src.profiles.schemas.input import ProfileInput
from src.profiles.schemas.update import ProfileUpdate


class ProfileManagementInterface(ABC):

    @abstractmethod
    def create_profile(self, profile_data: ProfileInput):
        pass

    @abstractmethod
    def read_all_profiles(self, page_size: int, page: int):
        pass

    @abstractmethod
    def find_profile_by_name(self, profile_name: str):
        pass

    @abstractmethod
    def update_profile(self, profile_data: ProfileUpdate):
        pass

    @abstractmethod
    def insert_new_vehicle(self, vehicle_id: str, profile_id: str):
        pass

    @abstractmethod
    def delete_profile(self, profile_id: str):
        pass
