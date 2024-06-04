from typing import Union

from src.profiles.interfaces.i_profile_validation import (ProfileNameValidationInterface,
                                                          ProfileUpdateValidationInterface)


class ProfileValidationController:
    def __init__(self, profile_data: Union[ProfileNameValidationInterface, ProfileUpdateValidationInterface]):
        self.__profile_data = profile_data

    def validate_profile_name(self):
        return self.__profile_data.validate_profile_name()

    def validate_profile_update(self):
        return self.__profile_data.profile_update_field_validator()
