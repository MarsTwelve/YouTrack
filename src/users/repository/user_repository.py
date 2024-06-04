from abc import ABC

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound

from src.users.schemas.input import UserInput
from src.users.interfaces.i_user_repository import UserRepositoryInterface
from src.users.schemas.login import UserLogin
from src.users.schemas.update import UserUpdate
from src.users.schemas.output import UserOutput
from src.Database.models import UserModel
from src.exeptions.custom_exeptions import BadRequestException


class SQLAlchemyUserRepository(UserRepositoryInterface, ABC):

    def __init__(self, session: Session):
        self.__session = session

    def insert_new_user(self, user_data: UserInput):
        user_model = UserModel(username=user_data.username,
                               password=user_data.password,
                               email=user_data.email,
                               language=user_data.language,
                               currency=user_data.currency,
                               country=user_data.country,
                               unit_speed=user_data.unit_speed,
                               unit_volume=user_data.unit_volume,
                               unit_length=user_data.unit_length,
                               unit_temp=user_data.unit_temp,
                               client_id=user_data.client_id)

        select_stmt = (select(UserModel)
                       .where(UserModel.username == user_data.username
                              or UserModel.password == user_data.password
                              or UserModel.email == user_data.email))

        result = self.__session.execute(select_stmt).first()
        if result:
            raise BadRequestException("[ERR]DUPLICATE - This user already exists.")

        self.__session.add(user_model)
        self.__session.commit()
        user_id = user_model.id
        self.__session.close()

        return f"user_id: {user_id}"

    def select_all_users(self, page: int, page_size: int):
        select_all = (select(UserModel)
                      .order_by(UserModel.username)
                      .limit(page_size).offset(page * page_size))

        result = self.__session.execute(select_all).scalars()
        for row in result:
            user_response = UserOutput(user_id=row.id,
                                       username=row.username,
                                       email=row.email,
                                       user_profile=row.profile_id)
            yield user_response

    def select_current_user(self, user_email: str):
        select_current = (select(UserModel)
                          .where(UserModel.email == user_email))

        result = self.__session.execute(select_current).scalar()
        user = UserOutput(user_id=result.id,
                          username=result.username,
                          email=result.email,
                          user_profile_id=result.profile_id)
        return user

    def select_user_by_name(self, user_name: str):
        select_by_name = (select(UserModel)
                          .where(UserModel.username.like(f"f%{user_name}%")))

        result = self.__session.execute(select_by_name).scalars()

        for row in result:
            user_response = UserOutput(user_id=row.id,
                                       username=row.username,
                                       email=row.email,
                                       user_profile_id=row.profile_id)
            yield user_response

    def select_user_login_information(self, user_data: UserLogin):
        select_stmt = select(UserModel).where(user_data.email == UserModel.email)
        result = self.__session.execute(select_stmt).scalar()
        return result

    def update_user(self, user_data: UserUpdate):
        update_field = user_data.update_field
        update_param = user_data.update_param
        update_stmt = (update(UserModel)
                       .values({update_field: update_param})
                       .where(UserModel.id == user_data.user_id))
        retrieve_updated = select(UserModel).where(UserModel.id == user_data.user_id)

        self.__session.execute(update_stmt)
        self.__session.commit()
        result = self.__session.execute(retrieve_updated).scalar()
        user = UserOutput(user_id=result.id,
                          username=result.username,
                          email=result.email,
                          user_profile_id=result.profile_id)
        return user

    def delete_user(self, user_id: str | None = None):
        select_delete = (select(UserModel)
                         .where(UserModel.id == user_id))
        user_to_delete = self.__session.execute(select_delete).scalar()

        if user_to_delete:
            # Delete the client
            self.__session.delete(user_to_delete)
            self.__session.commit()

            # Confirm deletion
            result_post_deletion = self.__session.execute(select_delete).first()
            if not result_post_deletion:
                return "User deleted successfully"

            else:
                return "[ERR]DELETION_ERROR - User deletion failed"  # TODO: Change to custom exception later (priority 2 - Yellow)
        return f"No profile found with id {user_id}"  # TODO: Change to custom exception later(priority 2 - Yellow)
