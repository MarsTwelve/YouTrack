import re
from abc import ABC

from src.clients.interfaces.i_validator import ClientNameValidationInterface
from src.exeptions.custom_exeptions import BadRequestException


class ClientNameValidation(ClientNameValidationInterface, ABC):
    def __init__(self, client_data: str):
        self.__client_name = client_data

    def format_spacing(self):
        truncate_spaces = re.sub(r"^\s+|\s+$", "", self.__client_name)
        validated_string = re.sub(r"\s{2,}", " ", truncate_spaces)
        self.__client_name = validated_string
        return self.__client_name

    def validate_invalid_chars(self):
        invalid_chars_pattern = r"[^A-z\s]"
        search = re.search(invalid_chars_pattern, self.__client_name)
        if search:
            return True
        return False

    def validate_name(self):
        base_response = "[ERR]VALIDATION_FAILED"
        self.format_spacing()

        if self.validate_invalid_chars():
            raise BadRequestException(base_response + " - Invalid characters are not allowed")
