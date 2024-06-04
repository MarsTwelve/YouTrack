from src.users.interfaces.i_user_service import UserManagementInterface
from src.users.schemas.input import UserInput
from src.users.schemas.update import UserUpdate
from src.users.schemas.login import UserLogin


class UserManagementController:
    def __init__(self, user_service: UserManagementInterface):
        self.__user_service = user_service

    def create_new_user(self, user_data: UserInput):
        return self.__user_service.create_user(user_data)

    def read_all_users(self, page:int, page_size: int):
        return self.__user_service.read_all_users(page, page_size)

    def find_user_by_name(self, user_name: str):
        return self.__user_service.find_user_by_name(user_name)

    def get_current_user(self, user_email: str):
        return self.__user_service.get_current_user(user_email)

    def get_login_info(self, user_data: UserLogin):
        return self.__user_service.get_user_login(user_data)

    def update_user(self, user_data: UserUpdate):
        return self.__user_service.update_user(user_data)

    def delete_user(self, user_id: str):
        return self.__user_service.delete_user(user_id)
