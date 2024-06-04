from abc import ABC

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.Database.models import ClientModel
from src.clients.schemas.input import ClientInput
from src.clients.schemas.output import ClientOutput
from src.clients.interfaces.i_client_repository import ClientRepositoryInterface
from src.clients.schemas.update import ClientUpdate
from src.exeptions.custom_exeptions import BadRequestException


class SQLAlchemyClientRepository(ClientRepositoryInterface, ABC):

    def __init__(self, session: Session):
        self.__session = session

    def insert_new_client(self, client_data: ClientInput):
        client_model = ClientModel(name=client_data.name,
                                   company_name=client_data.company_name,
                                   cellphone=client_data.cellphone,
                                   cpf_cnpj=client_data.cpf_cnpj)

        select_stmt = (select(ClientModel)
                       .where(ClientModel.name == client_data.name
                              or ClientModel.company_name == client_data.company_name
                              or ClientModel.cellphone == client_data.cellphone
                              or ClientModel.cpf_cnpj == client_data.cpf_cnpj))

        result = self.__session.execute(select_stmt).first()
        if result:
            raise BadRequestException("[ERR]DUPLICATE - This recipe already exists.")

        self.__session.add(client_model)
        self.__session.commit()
        client_id = client_model.id
        self.__session.close()

        return f"client_id: {client_id}"

    def select_all_clients(self, page: int, page_size: int):
        select_all = select(ClientModel).order_by(ClientModel.name).limit(page_size).offset(page * page_size)
        result = self.__session.execute(select_all).scalars()

        for row in result:
            client_response = ClientOutput(client_id=row.id,
                                           name=row.name,
                                           company_name=row.company_name,
                                           cellphone=row.cellphone,
                                           cpf_cnpj=row.cpf_cnpj)
            yield client_response

        self.__session.close()

    def select_client_by_name(self, client_name: str):
        select_client = select(ClientModel).where(ClientModel.name.like(f"%{client_name}%"))
        result = self.__session.execute(select_client).scalars()

        for row in result:
            client_response = ClientOutput(client_id=row.id,
                                           name=row.name,
                                           company_name=row.company_name,
                                           cellphone=row.cellphone,
                                           cpf_cnpj=row.cpf_cnpj)
            yield client_response

        self.__session.close()

    def update_client(self, client_data: ClientUpdate):
        update_field = client_data.update_field
        update_param = client_data.update_param
        update_stmt = (update(ClientModel)
                       .values({update_field: update_param})
                       .where(ClientModel.id == client_data.client_id))
        retrieve_updated = select(ClientModel).where(ClientModel.id == client_data.client_id)

        self.__session.execute(update_stmt)
        self.__session.commit()
        result = self.__session.execute(retrieve_updated).scalar()

        return result

    def delete_client(self, client_id: str):
        select_client = select(ClientModel).where(ClientModel.id == client_id)
        client = self.__session.execute(select_client).scalar()

        if client:
            # Delete the client
            self.__session.delete(client)
            self.__session.commit()

            # Confirm deletion
            result_post_deletion = self.__session.execute(select_client).first()
            if not result_post_deletion:
                return "Client deleted successfully"

            else:
                return "[ERR]DELETION_ERROR - Client deletion failed" # TODO: Change to custom exception later
        return f"No client found with id {client_id}" # TODO: Change to custom exception later
