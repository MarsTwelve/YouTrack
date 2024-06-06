from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional

from src.Database.operations import Database
from src.users.schemas.input import UserInput
from src.users.schemas.login import UserLogin
from src.users.schemas.update import UserUpdate
from src.users.schemas.output import UserOutput
from src.users.services.user_validation import UserValidatorService
from src.users.controller.user_validation import UserValidationController
from src.users.services.user_management import UserManagementService
from src.users.repository.user_repository import SQLAlchemyUserRepository
from src.users.controller.user_management import UserManagementController

from src.exeptions.custom_exeptions import (BadRequestException,
                                            DuplicateDataException)

from src.auth.schemas import Token
from src.auth.authentication import (authenticate_user,
                                     get_password_hash,
                                     get_token_timedelta,
                                     create_access_token,
                                     get_current_user,
                                     oauth2_scheme)

# TODO: multiple changes to be made to the client, such as
#  a new login method with oauth, similar to users, to better handle data and access points, implement a add_user
#  endpoint for relationship (priority 1 - black)


users_router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@users_router.post("/")
async def create_new_user(user_data: UserInput):
    validator_service = UserValidatorService(user_data)
    validator_controller = UserValidationController(validator_service)

    try:
        validator_controller.validate_user_data()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()

    hashed_password = get_password_hash(user_data.password)
    user_data.password = hashed_password

    repository = SQLAlchemyUserRepository(session)
    user_service = UserManagementService(repository)
    controller = UserManagementController(user_service)

    try:
        response = controller.create_new_user(user_data)
    except DuplicateDataException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.__str__())
    return response


@users_router.post("/login")
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user_login_data = UserLogin(email=form_data.username, password=form_data.password)

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyUserRepository(session)
    user_service = UserManagementService(repository)
    controller = UserManagementController(user_service)
    response = controller.get_login_info(user_login_data)

    if not response:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            headers={"X-message": "No results found"})

    # TODO: Make a UserInDB Model later to use with the db response
    user_in_db = {"email": response.email,
                  "hashed_password": response.password}

    authenticated = authenticate_user(user_login_data, user_in_db)
    if not authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="[ERR]LOGIN_FAILED - The email or password provided are incorrect")
    access_token_expires = get_token_timedelta()
    access_token = create_access_token(
        data={"sub": user_in_db["email"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@users_router.get("/")
async def get_users(current_user: Annotated[UserLogin, Depends(get_current_user)], page: int, page_size: int):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyUserRepository(session)
    user_service = UserManagementService(repository)
    controller = UserManagementController(user_service)

    response = controller.read_all_users(page, page_size)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@users_router.get("/search/{username}")
async def get_user_by_name(user_name: str):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyUserRepository(session)
    user_service = UserManagementService(repository)
    controller = UserManagementController(user_service)
    response = controller.find_user_by_name(user_name)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@users_router.get("/me")
async def get_user_me(current_user: Annotated[UserLogin, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyUserRepository(session)
    user_service = UserManagementService(repository)
    controller = UserManagementController(user_service)
    response = controller.get_current_user(current_user.payload_data)

    return response


@users_router.patch("/{user_id}")
async def update_user_info(current_user: Annotated[UserLogin, Depends(get_current_user)], user_data: UserUpdate):
    #TODO: implement validation for user_data, along with testing(priority 0 - red)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    if user_data.user_id:
        # TODO: check if user has admin permission, raise error if not (priority 1 - yellow)
        pass

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyUserRepository(session)
    user_service = UserManagementService(repository)
    controller = UserManagementController(user_service)
    user_id = controller.get_current_user(
        current_user.payload_data)  # TODO: change UserLogin to other model(priority 1 - green)
    user_data.user_id = user_id.user_id

    response = controller.update_user(user_data)

    return response


@users_router.delete("/{user_id}")
async def delete_user(current_user: Annotated[UserLogin, Depends(get_current_user)],
                      user_id: str | None = None):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[ERR]INVALID_CREDENTIALS - "
                                                                             "Could not validate user credentials")

    # TODO: Implement self deletion (if user_id == None) (priority 2 - green)

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyUserRepository(session)
    user_service = UserManagementService(repository)
    controller = UserManagementController(user_service)

    response = controller.delete_user(user_id)
    return response
