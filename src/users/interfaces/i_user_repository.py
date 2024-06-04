from abc import ABC, abstractmethod

from src.users.schemas.input import UserInput
from src.users.schemas.update import UserUpdate
from src.users.schemas.login import UserLogin


class UserRepositoryInterface(ABC):

    @abstractmethod
    def insert_new_user(self, user_data: UserInput):
        pass

    @abstractmethod
    def select_all_users(self, page: int, page_size: int):
        pass

    @abstractmethod
    def select_user_by_name(self, user_name: str):
        pass

    @abstractmethod
    def select_user_login_information(self, user_data: UserLogin):
        pass

    @abstractmethod
    def select_current_user(self, user_email: str):
        pass

    @abstractmethod
    def update_user(self, user_data: UserUpdate):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass
