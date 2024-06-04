from src.vehicles.interfaces.i_validator import VehicleValidatorInterface


class VehicleValidationController:

    def __init__(self, validate: VehicleValidatorInterface):
        self.validate = validate

    def validate_new_client(self):
        return self.validate.validate_vehicle_schema()
