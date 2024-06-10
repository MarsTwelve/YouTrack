from abc import ABC
import re

from src.clients.interfaces.i_validator import ClientUpdateValidationInterface
from src.exeptions.custom_exeptions import BadRequestException
from src.clients.schemas.update import ClientUpdate
from src.clients.services.cpf_validation import CPFValidationService


class ClientUpdateValidationService(ClientUpdateValidationInterface, ABC):

    def __init__(self, client_update: ClientUpdate):
        self.__client_update = client_update

    def format_spacing(self):
        for field_name, field_value in self.__client_update:
            truncate_spaces = re.sub(r"^\s+|\s+$", "", field_value)
            validated_string = re.sub(r"\s{2,}", " ", truncate_spaces)
            setattr(self.__client_update, field_name, validated_string)
        return self.__client_update

    def validate_invalid_chars(self):
        invalid_chars_pattern = r"[^A-z_\s\d]"

        search = re.search(invalid_chars_pattern, self.__client_update.update_param)
        if search:
            return True
        return False

    def validate_update_field(self):
        allowed_fields = ["name", "company_name", "cellphone", "cpf_cnpj"]
        if self.__client_update.update_field not in allowed_fields:
            return False
        return True

    def validate_cellphone_pattern(self):
        brazil_phone_pattern = r"^\+55\s\(\d{2}\)\s?9[\d]{8}"
        match_phone = re.match(brazil_phone_pattern, self.__client_update.update_param)
        if match_phone:
            return True
        return False

    def validate_update_parameters(self):
        if self.__client_update.update_field == "name" or self.__client_update.update_field == "company_name":
            return not self.validate_invalid_chars()
        return self.validate_cellphone_pattern()

    def validate_client_update_schema(self):
        base_response = "[ERR VALIDATION_FAILED]"

        if not self.validate_update_field():
            raise BadRequestException(base_response + " - This field doesn't allow updates, or doesn't exist")

        if not self.validate_update_parameters():
            if self.__client_update.update_field == "name" or self.__client_update.update_field == "company_name":
                raise BadRequestException(base_response + " - Special characters and digits are not allowed here"
                                                          f" --> {self.__client_update.update_field}")
            raise BadRequestException(base_response + " - This cellphone number is invalid")
