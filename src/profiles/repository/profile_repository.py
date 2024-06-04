from abc import ABC

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.profiles.schemas.input import ProfileInput
from src.profiles.schemas.update import ProfileUpdate
from src.profiles.schemas.output import ProfileOutput
from src.Database.models import ProfileModel
from src.profiles.interfaces.i_profile_repository import ProfileRepositoryInterface


class SQLAlchemyProfileRepository(ProfileRepositoryInterface, ABC):

    def __init__(self, session: Session):
        self.__session = session

    def insert_new_profile(self, profile_data: ProfileInput):
        profile_model = ProfileModel(profile_name=profile_data.profile_name,
                                     administrator=profile_data.administrator,
                                     fuel_avg=profile_data.fuel_avg,
                                     speed_avg=profile_data.speed_avg,
                                     route=profile_data.route,
                                     perimeters=profile_data.perimeters,
                                     tracking=profile_data.tracking,
                                     weather=profile_data.weather)

        self.__session.add(profile_model)
        self.__session.commit()
        profile_id = profile_model.id
        self.__session.close()
        return f"profile_id: {profile_id}"

    def select_all_profiles(self, page: int, page_size: int):
        select_all = (select(ProfileModel)
                      .order_by(ProfileModel.profile_name)
                      .limit(page_size).offset(page * page_size))
        result = self.__session.execute(select_all).scalars()

        for row in result:
            profile = ProfileOutput(profile_id=row.id,
                                    vehicle_id_list=row.vehicles,
                                    profile_name=row.profile_name,
                                    administrator=row.administrator,
                                    fuel_avg=row.fuel_avg,
                                    speed_avg=row.speed_avg,
                                    route=row.route,
                                    perimeters=row.perimeters,
                                    tracking=row.tracking,
                                    weather=row.weather)
            yield profile

        self.__session.close()

    def select_profile_by_name(self, profile_name: str):

        select_by_name = (select(ProfileModel)
                          .where(ProfileModel.profile_name.like(f"%{profile_name}%")))

        result = self.__session.execute(select_by_name).scalars()

        for row in result:
            profile_response = ProfileOutput(profile_id=row.id,
                                             vehicle_id_list=row.vehicles,
                                             profile_name=row.profile_name,
                                             administrator=row.administrator,
                                             fuel_avg=row.fuel_avg,
                                             speed_avg=row.speed_avg,
                                             route=row.route,
                                             perimeters=row.perimeters,
                                             tracking=row.tracking,
                                             weather=row.weather)
            yield profile_response

    def update_profile(self, profile_data: ProfileUpdate):
        update_field = profile_data.update_field
        update_param = profile_data.update_param
        update_stmt = (update(ProfileModel)
                       .values({update_field: update_param})
                       .where(ProfileModel.id == profile_data.profile_id))
        retrieve_updated = select(ProfileModel).where(ProfileModel.id == profile_data.profile_id)

        self.__session.execute(update_stmt)
        self.__session.commit()
        result = self.__session.execute(retrieve_updated).scalar()
        profile_response = ProfileOutput(profile_id=result.id,
                                         vehicle_id_list=result.vehicles,
                                         profile_name=result.profile_name,
                                         administrator=result.administrator,
                                         fuel_avg=result.fuel_avg,
                                         speed_avg=result.speed_avg,
                                         route=result.route,
                                         perimeters=result.perimeters,
                                         tracking=result.tracking,
                                         weather=result.weather)
        return profile_response

    def delete_profile(self, profile_id: str):
        select_delete = (select(ProfileModel)
                         .where(ProfileModel.id == profile_id))
        profile_to_delete = self.__session.execute(select_delete).scalar()

        if profile_to_delete:
            # Delete the client
            self.__session.delete(profile_to_delete)
            self.__session.commit()

            # Confirm deletion
            result_post_deletion = self.__session.execute(select_delete).first()
            if not result_post_deletion:
                return "Profile deleted successfully"

            else:
                return "[ERR]DELETION_ERROR - Profile deletion failed"  # TODO: Change to custom exception later (priority 2 - Yellow)
        return f"No profile found with id {profile_id}"  # TODO: Change to custom exception later(priority 2 - Yellow)



