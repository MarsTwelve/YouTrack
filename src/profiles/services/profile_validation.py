import re
from abc import ABC
from typing import Union

from src.exeptions.custom_exeptions import BadRequestException
from src.profiles.schemas.update import ProfileUpdate
from src.profiles.interfaces.i_profile_validation import (ProfileNameValidationInterface,
                                                          ProfileUpdateValidationInterface)


class ProfileNameValidationService(ProfileNameValidationInterface):
    def __init__(self, profile_name: str):
        self.__profile_name = profile_name

    def format_spacing(self, profile_name: str = None):
        truncate_spaces = re.sub(r"^\s+|\s+$", "", self.__profile_name)
        validated_string = re.sub(r"\s{2,}", " ", truncate_spaces)
        self.__profile_name = validated_string
        return self.__profile_name

    def validate_invalid_chars(self, profile_name: str = None):
        invalid_chars_pattern = r"[^A-z\s]"
        search = re.search(invalid_chars_pattern, self.__profile_name)
        if search:
            return True
        return False

    def validate_profile_name(self):
        base_response = "[ERR]VALIDATION_FAILED"
        self.format_spacing()
        if self.validate_invalid_chars():
            raise BadRequestException(base_response + " - Invalid characters are not allowed")
        return True


class ProfileUpdateValidationService(ProfileUpdateValidationInterface, ABC):
    def __init__(self, profile_data: ProfileUpdate):
        self.__profile_data = profile_data

    def format_spacing(self, profile_name: str = None):
        truncate_spaces = re.sub(r"^\s+|\s+$", "", profile_name)
        validated_string = re.sub(r"\s{2,}", " ", truncate_spaces)
        return validated_string

    def validate_invalid_chars(self, profile_name: str = None):
        invalid_chars_pattern = r"[^A-z\s]"
        search = re.search(invalid_chars_pattern, profile_name)
        if search:
            return True
        return False

    def profile_id_validator(self):
        if len(self.__profile_data.profile_id) != 32:
            return False
        return True

    def profile_update_field_validator(self):
        valid_fields = ["profile_name", "administrator", "fuel_avg", "speed_avg",
                        "route", "perimeters", "tracking", "weather"]

        if self.__profile_data.update_field not in valid_fields:
            return False
        return True

    def profile_update_param_validator(self):
        if self.__profile_data.update_field == "profile_name":
            formatted_name = self.format_spacing(self.__profile_data.update_field)
            return self.validate_invalid_chars(formatted_name)

        if not isinstance(self.__profile_data.update_param, bool):
            return False
        return True

    def validate_profile_update(self):
        base_response = "[ERR]VALIDATION_FAILED"

        if not self.profile_id_validator():
            raise BadRequestException(base_response + " - the id provided is invalid")

        if not self.profile_update_field_validator():
            raise BadRequestException(base_response + " - this field doesn't exist or isn't allowed  to be updated")

        if not self.profile_update_param_validator():
            raise BadRequestException(base_response + " - this parameter is invalid")
