from fastapi import APIRouter, status, Response, HTTPException
from src.Database.operations import Database
from src.clients.schemas.input import ClientInput
from src.clients.schemas.update import ClientUpdate
from src.clients.services.new_client_validation import ClientValidatorService
from src.clients.services.client_name_validation import ClientNameValidation
from src.clients.services.client_management import ClientManagementService
from src.clients.services.client_update_validation import ClientUpdateService
from src.clients.repository.client_repository import SQLAlchemyClientRepository
from src.clients.controller.client_management import ClientManagementController
from src.clients.controller.validation import (NewClientValidationController,
                                               ClientNameValidationController,
                                               ClientUpdateValidationController)
from src.exeptions.custom_exeptions import BadRequestException

client_router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@client_router.post("/")
async def create_new_client(client_data: ClientInput):
    validation_service = ClientValidatorService(client_data)
    controller = NewClientValidationController(validation_service)

    try:
        controller.validate_new_client()  # TODO:refactor to better naming
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
    return response


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
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    return first_item, response


@client_router.patch("/{client_id}")
async def update_client_info(client_data: ClientUpdate):
    validation_service = ClientUpdateService(client_data)
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
    # TODO: add validation to the delete DTO
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
