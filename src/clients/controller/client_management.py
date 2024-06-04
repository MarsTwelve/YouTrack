from src.clients.schemas.input import ClientInput
from src.clients.schemas.update import ClientUpdate
from src.clients.interfaces.i_client_service import ClientManagementInterface


class ClientManagementController:
    def __init__(self, client_service: ClientManagementInterface):
        self.__client_service = client_service

    def create_new_client(self, client_data: ClientInput):
        return self.__client_service.create_client(client_data)

    def get_all_clients(self, page: int, page_size: int):
        return self.__client_service.read_all_clients(page, page_size)

    def get_client_by_name(self, client_name: str):
        return self.__client_service.find_client_by_name(client_name)

    def update_client_info(self, client_data: ClientUpdate):
        return self.__client_service.update_client(client_data)

    def delete_client(self, client_id: str):
        return self.__client_service.delete_client(client_id)
