import re
from datetime import datetime
from abc import ABC

from src.vehicles.interfaces.i_validator import VehicleValidatorInterface


class VehicleValidationService(VehicleValidatorInterface, ABC):
    def __init__(self, vehicle_data):
        self.__vehicle_data = vehicle_data

    def format_spacing(self):
        for field_name, field_value in self.__vehicle_data:
            if field_name == "manufacture_year":
                continue
            truncate_spaces = re.sub(r"^\s+|\s+$", "", field_value)
            validated_string = re.sub(r"\s{2,}", " ", truncate_spaces)
            setattr(self.__vehicle_data, field_name, validated_string)
        return self.__vehicle_data

    def validate_invalid_chars(self):
        invalid_chars_pattern = r"[^A-z\s\d?]"
        for field_name, field_value in self.__vehicle_data:
            if field_name == "manufacture_year" or field_name == "number_plate":
                continue
            search = re.search(invalid_chars_pattern, field_value)
            if search:
                return True
        return False

    def validate_manufacture_year(self):
        if self.__vehicle_data.manufacture_year > datetime.now().year:
            return False
        return True

    def validate_plate_format(self):
        mercosul_plate_format = r"[A-Z]{3}\d[A-Z]\d{2}"
        plate_match = re.match(mercosul_plate_format, self.__vehicle_data.number_plate)
        if plate_match:
            return True
        return False

    def validate_vehicle_schema(self):
        base_response = "[ERR]VALIDATION_FAILED"
        self.format_spacing()

        if self.validate_invalid_chars():
            return base_response

        if not self.validate_manufacture_year():
            return base_response

        if not self.validate_plate_format():
            return base_response
        return True
