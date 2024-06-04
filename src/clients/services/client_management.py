from abc import ABC

from src.clients.schemas.input import ClientInput
from src.clients.schemas.update import ClientUpdate
from src.clients.interfaces.i_client_service import ClientManagementInterface
from src.clients.interfaces.i_client_repository import ClientRepositoryInterface


class ClientManagementService(ClientManagementInterface, ABC):

    def __init__(self, repository: ClientRepositoryInterface):
        self.__repository = repository

    def create_client(self, client_data: ClientInput):
        return self.__repository.insert_new_client(client_data)

    def read_all_clients(self, page: int, page_size: int):
        return self.__repository.select_all_clients(page, page_size)

    def find_client_by_name(self, client_name: str):
        return self.__repository.select_client_by_name(client_name)

    def update_client(self, client_data: ClientUpdate):
        return self.__repository.update_client(client_data)

    def delete_client(self, client_id: str):
        return self.__repository.delete_client(client_id)
