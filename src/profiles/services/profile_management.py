
from src.profiles.interfaces.i_profile_service import ProfileManagementInterface
from src.profiles.interfaces.i_profile_repository import ProfileRepositoryInterface
from src.profiles.schemas.input import ProfileInput
from src.profiles.schemas.update import ProfileUpdate


class ProfileManagementService(ProfileManagementInterface):

    def __init__(self, repository: ProfileRepositoryInterface):
        self.__repository = repository

    def create_profile(self, profile_data: ProfileInput):
        return self.__repository.insert_new_profile(profile_data)

    def read_all_profiles(self, page_size: int, page: int):
        return self.__repository.select_all_profiles(page_size, page)

    def find_profile_by_name(self, profile_name: str):
        return self.__repository.select_profile_by_name(profile_name)

    def update_profile(self, profile_data: ProfileUpdate):
        return self.__repository.update_profile(profile_data)

    def insert_new_vehicle(self, vehicle_id: str, profile_id: str):
        return self.__repository.insert_new_vehicle(vehicle_id, profile_id)

    def delete_profile(self, profile_id: str):
        return self.__repository.delete_profile(profile_id)
