from abc import ABC, abstractmethod
from typing import Union

from src.profiles.schemas.update import ProfileUpdate


class BaseProfileValidationInterface(ABC):
    @abstractmethod
    def format_spacing(self, profile_name: str = None):
        pass

    @abstractmethod
    def validate_invalid_chars(self, profile_name: str = None):
        pass


class ProfileNameValidationInterface(BaseProfileValidationInterface):
    @abstractmethod
    def validate_profile_name(self):
        pass


class ProfileUpdateValidationInterface(BaseProfileValidationInterface):
    @abstractmethod
    def profile_id_validator(self):
        pass

    @abstractmethod
    def profile_update_field_validator(self):
        pass

    @abstractmethod
    def profile_update_param_validator(self):
        pass
