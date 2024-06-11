from abc import ABC

from sqlalchemy import select, update, and_
from sqlalchemy.orm import Session

from src.Database.models import VehicleModel


from src.vehicles.interfaces.i_vehicle_repository import VehicleRepositoryInterface
from src.vehicles.schemas.input import VehicleInput
from src.vehicles.schemas.search import VehicleSearch
from src.vehicles.schemas.update import VehicleUpdate
from src.vehicles.schemas.output import VehicleOutput


class SQLAlchemyVehicleRepository(VehicleRepositoryInterface, ABC):
    def __init__(self, session: Session):
        self.__session = session

    def insert_new_vehicle(self, vehicle_data: VehicleInput):
        vehicle_model = VehicleModel(vehicle_make=vehicle_data.vehicle_make,
                                     vehicle_model=vehicle_data.vehicle_model,
                                     vehicle_trim=vehicle_data.vehicle_trim,
                                     vehicle_color=vehicle_data.vehicle_color,
                                     model_year=vehicle_data.manufacture_year,
                                     number_plate=vehicle_data.number_plate,
                                     client_id=vehicle_data.client_id)

        self.__session.add(vehicle_model)
        self.__session.commit()
        vehicle_id = vehicle_model.id
        self.__session.close()
        return f"vehicle_id: {vehicle_id}"

    def select_all_vehicles(self, page: int, page_size: int):
        select_all = (select(VehicleModel)
                      .order_by(VehicleModel.vehicle_model)
                      .limit(page_size).offset(page * page_size))
        result = self.__session.execute(select_all).scalars()

        for row in result:
            vehicle_response = VehicleOutput(vehicle_id=row.id,
                                             client_id=row.client_id,
                                             profile_id="fix later, need relationship",
                                             vehicle_make=row.vehicle_make,
                                             vehicle_model=row.vehicle_model,
                                             vehicle_trim=row.vehicle_trim,
                                             vehicle_color=row.vehicle_color,
                                             manufacture_year=row.model_year,
                                             number_plate=row.number_plate)

            yield vehicle_response

        self.__session.close()

    def select_vehicle_by_id(self, vehicle_id: str):
        select_vehicle = (select(VehicleModel)
                          .where(VehicleModel.id == vehicle_id))

        result = self.__session.execute(select_vehicle).scalar()
        return result

    def select_vehicle_by_search_criteria(self, vehicle_data: VehicleSearch):
        result = None

        if not vehicle_data.model:
            select_brand = (select(VehicleModel)
                            .where(VehicleModel.vehicle_make.like(f"%{vehicle_data.make}%")))
            result = self.__session.execute(select_brand).scalars()

        if vehicle_data.model:
            select_model = (select(VehicleModel)
                            .where(and_(VehicleModel.vehicle_model.like(f"%{vehicle_data.model}%"),
                                        VehicleModel.vehicle_make).like(f"%{vehicle_data.make}%")))
            result = self.__session.execute(select_model).scalars()

        if not result:
            return "Not Found error" # TODO: Properly add the 204 not found error (priority 1)

        for row in result:
            specific_profile = row.profiles[0]
            vehicle_response = VehicleOutput(vehicle_id=row.id,
                                             client_id=row.client_id,
                                             profile_id=specific_profile.id,
                                             vehicle_make=row.vehicle_make,
                                             vehicle_model=row.vehicle_model,
                                             vehicle_trim=row.vehicle_trim,
                                             vehicle_color=row.vehicle_color,
                                             manufacture_year=row.model_year,
                                             number_plate=row.number_plate)
            yield vehicle_response

    def update_vehicle_info(self, vehicle_data: VehicleUpdate):
        update_field = vehicle_data.update_field
        update_param = vehicle_data.update_param
        update_stmt = (update(VehicleModel)
                       .values({update_field: update_param})
                       .where(VehicleModel.id == vehicle_data.vehicle_id))
        retrieve_updated = select(VehicleModel).where(VehicleModel.id == vehicle_data.vehicle_id)

        self.__session.execute(update_stmt)
        self.__session.commit()
        result = self.__session.execute(retrieve_updated).scalar()
        vehicle_response = VehicleOutput(vehicle_id=result.id,
                                         client_id=result.client_id,
                                         profile_id="Fix later",
                                         vehicle_make=result.vehicle_make,
                                         vehicle_model=result.vehicle_model,
                                         vehicle_trim=result.vehicle_trim,
                                         vehicle_color=result.vehicle_color,
                                         manufacture_year=result.model_year,
                                         number_plate=result.number_plate)
        return vehicle_response

    def delete_vehicle(self, vehicle_id: str):
        select_delete = (select(VehicleModel)
                         .where(VehicleModel.id == vehicle_id))
        vehicle_to_delete = self.__session.execute(select_delete).scalar()

        if vehicle_to_delete:
            # Delete the vehicle
            self.__session.delete(vehicle_to_delete)
            self.__session.commit()

            # Confirm deletion
            result_post_deletion = self.__session.execute(select_delete).first()
            if not result_post_deletion:
                return "Vehicle deleted successfully"

            else:
                return "[ERR]DELETION_ERROR - Vehicle deletion failed"  # TODO: Change to custom exception later (priority 2 - Yellow)
        return f"No vehicle found with id {vehicle_id}"  # TODO: Change to custom exception later(priority 2 - Yellow)
