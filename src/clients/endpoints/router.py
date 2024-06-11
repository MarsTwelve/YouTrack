from fastapi import APIRouter, status, HTTPException

from src.Database.operations import Database
from src.exeptions.custom_exeptions import BadRequestException

from src.clients.schemas.input import ClientInput
from src.clients.schemas.update import ClientUpdate

from src.clients.services.new_client_validation import ClientValidatorService
from src.clients.services.client_name_validation import ClientNameValidation
from src.clients.services.client_management import ClientManagementService
from src.clients.services.client_update_validation import ClientUpdateValidationService
from src.clients.services.cpf_validation import CPFValidationService
from src.clients.services.cnpj_validation import CNPJValidationService

from src.clients.repository.client_repository import SQLAlchemyClientRepository
from src.clients.controller.client_management import ClientManagementController
from src.clients.controller.validation import (NewClientValidationController,
                                               ClientNameValidationController,
                                               ClientUpdateValidationController)

client_router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@client_router.post("/")
async def create_new_client(client_data: ClientInput):
    cpf_validation_service = CPFValidationService(client_data.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client_data.cpf_cnpj)
    validation_service = ClientValidatorService(client_data, cpf_validation_service, cnpj_validation_service)
    controller = NewClientValidationController(validation_service)

    try:
        controller.validate_new_client()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()
    repository = SQLAlchemyClientRepository(session)

    client_service = ClientManagementService(repository)
    controller = ClientManagementController(client_service)
    try:
        response = controller.create_new_client(client_data)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.__str__())
    return response


@client_router.get("/")
async def get_clients(page: int = 1, page_size: int = 5):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyClientRepository(session)
    client_service = ClientManagementService(repository)
    controller = ClientManagementController(client_service)
    response = controller.get_all_clients(page, page_size)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@client_router.get("/{name}", status_code=status.HTTP_200_OK)
async def get_clients_by_name(client_name: str):
    validation_service = ClientNameValidation(client_name)
    controller = ClientNameValidationController(validation_service)

    try:
        controller.validate_client_name()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyClientRepository(session)
    client_service = ClientManagementService(repository)
    controller = ClientManagementController(client_service)
    response = controller.get_client_by_name(client_name)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@client_router.patch("/{client_id}")
async def update_client_info(client_data: ClientUpdate):
    validation_service = ClientUpdateValidationService(client_data)
    controller = ClientUpdateValidationController(validation_service)

    try:
        controller.validate_client_update()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyClientRepository(session)
    client_service = ClientManagementService(repository)
    controller = ClientManagementController(client_service)
    response = controller.update_client_info(client_data)
    return response


@client_router.delete("/{client_id}", status_code=status.HTTP_200_OK)
async def delete_client(client_id):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyClientRepository(session)
    client_service = ClientManagementService(repository)
    controller = ClientManagementController(client_service)
    try:
        data = controller.delete_client(client_id)
        return data
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())
