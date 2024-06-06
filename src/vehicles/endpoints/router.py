from fastapi import APIRouter

from src.Database.operations import Database

from src.vehicles.schemas.input import VehicleInput
from src.vehicles.schemas.search import VehicleSearch
from src.vehicles.schemas.update import VehicleUpdate

from src.vehicles.controller.validation import VehicleValidationController
from src.vehicles.services.validation import VehicleValidationService

from src.vehicles.controller.vehicle_management import VehicleManagementController
from src.vehicles.services.vehicle_management import VehicleManagementService
from src.vehicles.repository.vehicle_repository import SQLAlchemyVehicleRepository

from src.auth.authentication import get_current_user

vehicles_router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"]
)


@vehicles_router.post("/")
async def create_new_vehicle(vehicle_data: VehicleInput):
    #TODO: implement current user, later make a select to get the client_id (priority 0 - yellow)

    validation_service = VehicleValidationService(vehicle_data)
    controller = VehicleValidationController(validation_service)

    try:
        controller.validate.validate_vehicle_schema()
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())

    db = Database()
    session = db.get_session()

    repository = SQLAlchemyVehicleRepository(session)
    vehicle_service = VehicleManagementService(repository)
    controller = VehicleManagementController(vehicle_service)

    response = controller.create_vehicle(vehicle_data)
    return response


@vehicles_router.get("/")
async def get_vehicles(page: int, page_size: int):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyVehicleRepository(session)
    vehicle_service = VehicleManagementService(repository)
    controller = VehicleManagementController(vehicle_service)
    response = controller.read_all_vehicles(page, page_size)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@vehicles_router.get("/{vehicle_name}")
async def get_vehicle_by_name(vehicle_data: VehicleSearch):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyVehicleRepository(session)
    vehicle_service = VehicleManagementService(repository)
    controller = VehicleManagementController(vehicle_service)
    response = controller.find_vehicle_by_name(vehicle_data)

    try:
        first_item = next(response)
        remaining_items = list(response)
    except StopIteration:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, headers={"X-Message": "No results found"})
    remaining_items.insert(0, first_item)
    return remaining_items


@vehicles_router.patch("/{vehicle_id}")
async def update_vehicle_info(vehicle_data: VehicleUpdate):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyVehicleRepository(session)
    vehicle_service = VehicleManagementService(repository)
    controller = VehicleManagementController(vehicle_service)

    response = controller.update_vehicle(vehicle_data)
    return response


@vehicles_router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: str):
    db = Database()
    session = db.get_session()

    repository = SQLAlchemyVehicleRepository(session)
    vehicle_service = VehicleManagementService(repository)
    controller = VehicleManagementController(vehicle_service)

    response = controller.delete_vehicle(vehicle_id)
    return response
