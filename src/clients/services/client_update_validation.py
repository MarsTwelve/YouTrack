from abc import ABC
import re

from src.clients.interfaces.i_validator import ClientUpdateValidationInterface
from src.exeptions.custom_exeptions import BadRequestException
from src.clients.schemas.update import ClientUpdate
from src.clients.services.new_client_validation import CPFValidator, CNPJValidator


class ClientUpdateService(ClientUpdateValidationInterface, ABC):
    allowed_fields = ["name", "company_name", "cellphone", "cpf_cnpj"]

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

        for field_name, field_value in self.__client_update:
            search = re.search(invalid_chars_pattern, field_value)
            if search:
                return True
        return False

    def validate_update_field(self):
        base_response = "[ERR VALIDATION_FAILED]"
        if self.__client_update.update_field not in self.allowed_fields:
            raise BadRequestException(base_response + " - This field doesn't allow updates, or doesn't exist")

    def validate_update_parameters(self):
        pass
