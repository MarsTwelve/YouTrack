from abc import ABC, abstractmethod

from src.users.schemas.input import UserInput
from src.users.schemas.update import UserUpdate
from src.users.schemas.login import UserLogin


class UserManagementInterface(ABC):

    @abstractmethod
    def create_user(self, user_data: UserInput):
        pass

    @abstractmethod
    def read_all_users(self, page: int, page_size: int):
        pass

    @abstractmethod
    def find_user_by_name(self, user_name: str):
        pass

    @abstractmethod
    def get_user_login(self, user_data: UserLogin):
        pass

    @abstractmethod
    def get_current_user(self, user_email: str):
        pass

    @abstractmethod
    def update_user(self, user_data: UserUpdate):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass
