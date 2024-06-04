from abc import ABC, abstractmethod

from src.profiles.schemas.input import ProfileInput
from src.profiles.schemas.update import ProfileUpdate


class ProfileRepositoryInterface(ABC):

    @abstractmethod
    def insert_new_profile(self, profile_data: ProfileInput):
        pass

    @abstractmethod
    def select_all_profiles(self, page_size: int, page: int):
        pass

    @abstractmethod
    def select_profile_by_name(self, profile_name: str):
        pass

    @abstractmethod
    def update_profile(self, profile_data: ProfileUpdate):
        pass

    @abstractmethod
    def delete_profile(self, profile_id: str):
        pass
