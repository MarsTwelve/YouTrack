from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from src.users.schemas.login import UserLogin
from src.Database.operations import Database
from src.auth.schemas import Token
from src.auth.authentication import get_current_user
from src.exeptions.custom_exeptions import BadRequestException

from src.profiles.schemas.input import ProfileInput
from src.profiles.schemas.update import ProfileUpdate
from src.profiles.services.profile_management import ProfileManagementService
from src.profiles.services.profile_validation import (ProfileNameValidationService,
                                                      ProfileUpdateValidationService)
from src.profiles.repository.profile_repository import SQLAlchemyProfileRepository
from src.profiles.controller.profile_management import ProfileManagementController
from src.profiles.controller.profile_validation import ProfileValidationController

profile_router = APIRouter(
    prefix="/profile",
    tags=["profiles"]
)


@profile_router.post("/")
async def create_new_profile(current_user: Annotated[UserLogin, Depends(get_current_user)], profile_data: ProfileInput):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    validation_service = ProfileNameValidationService(profile_data.profile_name)
    controller = ProfileValidationController(validation_service)

    try:
        controller.validate_profile_name()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyProfileRepository(session)
    client_service = ProfileManagementService(repository)
    controller = ProfileManagementController(client_service)
    response = controller.create_new_profile(profile_data)
    return response


@profile_router.get("/")
async def get_profiles(page_size: int, page: int):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyProfileRepository(session)
    profile_service = ProfileManagementService(repository)
    controller = ProfileManagementController(profile_service)

    response = controller.read_all_profiles(page, page_size)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@profile_router.get("/{profile_name}")
async def get_profile_by_name(current_user: Annotated[UserLogin, Depends(get_current_user)], profile_name: str):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    validation_service = ProfileNameValidationService(profile_name)
    controller = ProfileValidationController(validation_service)

    try:
        controller.validate_profile_name()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyProfileRepository(session)
    client_service = ProfileManagementService(repository)
    controller = ProfileManagementController(client_service)
    response = controller.find_profile_by_name(profile_name)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@profile_router.patch("/{profile_id}")
async def update_profile(current_user: Annotated[UserLogin, Depends(get_current_user)], profile_data: ProfileUpdate):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    validation_service = ProfileUpdateValidationService(profile_data)
    controller = ProfileValidationController(validation_service)

    try:
        controller.validate_profile_update()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyProfileRepository(session)
    profile_service = ProfileManagementService(repository)
    controller = ProfileManagementController(profile_service)

    response = controller.update_profile(profile_data)
    return response


@profile_router.delete("/{profile_id}")
async def delete_profile(current_user: Annotated[UserLogin, Depends(get_current_user)], profile_id: str):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyProfileRepository(session)
    client_service = ProfileManagementService(repository)
    controller = ProfileManagementController(client_service)

    response = controller.delete_profile(profile_id)
    return response
