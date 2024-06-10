import re
from abc import ABC

from src.clients.interfaces.i_validator import (NewClientValidationInterface,
                                                CPFCNPJValidatorInterface)
from src.exeptions.custom_exeptions import BadRequestException
from src.clients.schemas.input import ClientInput


class ClientValidatorService(NewClientValidationInterface, ABC):
    def __init__(self, client_data: ClientInput, cpf_validation_service: CPFCNPJValidatorInterface,
                 cnpj_validation_service: CPFCNPJValidatorInterface):
        self.__client = client_data
        self.__cpf_validation = cpf_validation_service
        self.__cnpj_validation = cnpj_validation_service

    def format_spacing(self):
        for field_name, field_value in self.__client:
            truncate_spaces = re.sub(r"^\s+|\s+$", "", field_value)
            validated_string = re.sub(r"\s{2,}", " ", truncate_spaces)
            setattr(self.__client, field_name, validated_string)
        return self.__client

    def validate_invalid_chars(self):
        invalid_chars_pattern = r"[^A-z\s]"

        for field_name, field_value in self.__client:
            if field_name == "cellphone" or field_name == "cpf_cnpj":
                continue
            search = re.search(invalid_chars_pattern, field_value)
            if search:
                return True
        return False

    def validate_cellphone_pattern(self):
        brazil_phone_pattern = r"^\+55\s\(\d{2}\)\s?9[\d]{8}"
        match_phone = re.match(brazil_phone_pattern, self.__client.cellphone)
        if match_phone:
            return True
        return False

    def validate_new_client_schema(self):
        base_response = "[ERR]VALIDATION_FAILED"
        self.format_spacing()

        if self.validate_invalid_chars():
            raise BadRequestException(base_response + " - Invalid characters are not allowed")

        if not self.validate_cellphone_pattern():
            raise BadRequestException(base_response + " - This cellphone number is invalid")

        if self.__cpf_validation.validate_pattern():
            if self.__cpf_validation.validate_digits():
                return True
            raise BadRequestException(base_response + " - This cpf number is invalid")

        if self.__cnpj_validation.validate_pattern():
            if self.__cnpj_validation.validate_digits():
                return True
            raise BadRequestException(base_response + " - This cnpj number is invalid")

        return False
