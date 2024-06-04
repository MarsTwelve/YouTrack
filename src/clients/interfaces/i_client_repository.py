from abc import ABC, abstractmethod

from src.clients.schemas.input import ClientInput
from src.clients.schemas.update import ClientUpdate


class ClientRepositoryInterface(ABC):

    @abstractmethod
    def insert_new_client(self, client_data: ClientInput):
        pass

    @abstractmethod
    def select_all_clients(self, page: int, page_size: int):
        pass

    @abstractmethod
    def select_client_by_name(self, client_name: str):
        pass

    @abstractmethod
    def update_client(self, client_data: ClientUpdate):
        pass

    @abstractmethod
    def delete_client(self, client_id: str):
        pass
