from abc import ABC

from src.users.interfaces.i_user_service import UserManagementInterface
from src.users.interfaces.i_user_repository import UserRepositoryInterface

from src.users.schemas.input import UserInput
from src.users.schemas.update import UserUpdate
from src.users.schemas.login import UserLogin


class UserManagementService(UserManagementInterface, ABC):

    def __init__(self, repository: UserRepositoryInterface):
        self.__repository = repository

    def create_user(self, user_data: UserInput):
        return self.__repository.insert_new_user(user_data)

    def read_all_users(self, page: int, page_size: int):
        return self.__repository.select_all_users(page, page_size)

    def find_user_by_name(self, user_name: str):
        return self.__repository.select_user_by_name(user_name)

    def get_current_user(self, user_email: str):
        return self.__repository.select_current_user(user_email)

    def get_user_login(self, user_data: UserLogin):
        return self.__repository.select_user_login_information(user_data)

    def update_user(self, user_data: UserUpdate):
        return self.__repository.update_user(user_data)

    def delete_user(self, user_id: str):
        return self.__repository.delete_user(user_id)
