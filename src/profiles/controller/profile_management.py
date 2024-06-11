from src.profiles.interfaces.i_profile_service import ProfileManagementInterface
from src.profiles.schemas.input import ProfileInput
from src.profiles.schemas.update import ProfileUpdate


class ProfileManagementController:
    def __init__(self, profile_service: ProfileManagementInterface):
        self.__profile_service = profile_service

    def create_new_profile(self, profile_data: ProfileInput):
        return self.__profile_service.create_profile(profile_data)

    def read_all_profiles(self, page_size: int, page: int):
        return self.__profile_service.read_all_profiles(page_size, page)

    def find_profile_by_name(self, profile_name: str):
        return self.__profile_service.find_profile_by_name(profile_name)

    def update_profile(self, profile_data: ProfileUpdate):
        return self.__profile_service.update_profile(profile_data)

    def add_vehicle_to_profile(self, vehicle_id, profile_id: str):
        return self.__profile_service.insert_new_vehicle(vehicle_id, profile_id)

    def delete_profile(self, profile_id: str):
        return self.__profile_service.delete_profile(profile_id)
