from abc import ABC, abstractmethod


class VehicleValidatorInterface(ABC):

    @abstractmethod
    def format_spacing(self):
        pass

    @abstractmethod
    def validate_invalid_chars(self):
        pass

    @abstractmethod
    def validate_manufacture_year(self):
        pass

    @abstractmethod
    def validate_plate_format(self):
        pass

    @abstractmethod
    def validate_vehicle_schema(self):
        pass
