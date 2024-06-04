from abc import ABC, abstractmethod

from src.clients.schemas.input import ClientInput
from src.clients.schemas.update import ClientUpdate
from src.clients.schemas.output import ClientOutput


class ClientManagementInterface(ABC):

    @abstractmethod
    def create_client(self, client_data: ClientInput):
        pass

    @abstractmethod
    def read_all_clients(self, page: int, page_size: int):
        pass

    @abstractmethod
    def find_client_by_name(self, client_name: str):
        pass

    @abstractmethod
    def update_client(self, client_data: ClientUpdate):
        pass

    @abstractmethod
    def delete_client(self, client_id):
        pass
