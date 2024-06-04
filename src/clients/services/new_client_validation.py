import re
from abc import ABC

from src.clients.interfaces.i_validator import NewClientValidationInterface
from src.exeptions.custom_exeptions import BadRequestException


class ClientValidatorService(NewClientValidationInterface, ABC):
    def __init__(self, client_data):
        self.__client = client_data

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

    def validate_cpf(self):
        validate = CPFValidator(self.__client.cpf_cnpj)
        if validate.validate_pattern():
            if validate.validate_digits():
                return True
        return False

    def validate_cnpj(self):
        validate = CNPJValidator(self.__client.cpf_cnpj)
        if validate.validate_pattern():
            if validate.validate_digits():
                return True
        return False

    def is_valid(self):
        base_response = "[ERR]VALIDATION_FAILED"
        self.format_spacing()
        if self.validate_invalid_chars():
            raise BadRequestException(base_response + " - Invalid characters are not allowed")

        if not self.validate_cellphone_pattern():
            raise BadRequestException(base_response + " - This cellphone number is invalid")

        if not self.validate_cpf():
            if not self.validate_cnpj():
                raise BadRequestException(base_response + " - This cpf number is invalid")
        return True


class CNPJValidator:

    def __init__(self, cnpj_string):
        self.cnpj = cnpj_string
        self.calculated_cnpj = None
        self.__cnpj_no_digit = None

    def __remove_dots_hyphen(self):
        no_dots_hyphen = re.sub(r"[.\-/]", "", self.cnpj)
        self.cnpj = no_dots_hyphen

    def __remove_last_digits(self):
        self.__remove_dots_hyphen()
        self.__cnpj_no_digit = self.cnpj[:-2]

    def __calculate_first_digit(self):
        multiplier = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total_sum = 0
        divisor = 11

        for i in range(len(self.__cnpj_no_digit)):
            number = int(self.__cnpj_no_digit[i])
            total_sum += number * multiplier[i]
        remainder = total_sum % divisor
        first_digit = divisor - remainder
        if remainder < 2:
            first_digit = 0
        return str(first_digit)

    def __calculate_second_digit(self):
        multiplier = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total_sum = 0
        divisor = 11

        cnpj_w_first_digit = self.__cnpj_no_digit + self.__calculate_first_digit()
        for i in range(len(cnpj_w_first_digit)):
            number = int(cnpj_w_first_digit[i])
            total_sum += number * multiplier[i]
        remainder = total_sum % divisor
        second_digit = divisor - remainder
        if remainder < 2:
            second_digit = 0
        self.calculated_cnpj = cnpj_w_first_digit + str(second_digit)

    def validate_pattern(self):
        cnpj_pattern = r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}"
        match_cnpj = re.match(cnpj_pattern, self.cnpj)
        if match_cnpj:
            return True
        return False

    def validate_digits(self):
        self.__remove_last_digits()
        self.__calculate_second_digit()

        if self.calculated_cnpj == self.cnpj:
            return True
        return False


class CPFValidator:

    def __init__(self, cpf_string: str):
        self.cpf = cpf_string
        self.calculated_cpf = None
        self.__cpf_no_digit = None

    def __remove_dots_hyphen(self):
        no_dots_hyphen = re.sub(r"[.-]", "", self.cpf)
        self.cpf = no_dots_hyphen

    def __remove_last_digits(self):
        self.__remove_dots_hyphen()
        self.__cpf_no_digit = self.cpf[:-2]

    def __calculate_first_digit(self):
        multiplier = 10
        total_sum = 0
        divisor = 11

        for number in self.__cpf_no_digit:
            if multiplier == 1:
                break
            number = int(number)
            total_sum += number * multiplier
            multiplier -= 1
        first_digit = divisor - total_sum % divisor
        if first_digit < 2:
            first_digit = 0
        return str(first_digit)

    def __calculate_second_digit(self):
        multiplier = 11
        total_sum = 0
        divisor = 11

        cpf_w_first_digit = self.__cpf_no_digit + self.__calculate_first_digit()
        for number in cpf_w_first_digit:
            if multiplier == 1:
                break
            number = int(number)
            total_sum += number * multiplier
            multiplier -= 1
        remainder = total_sum % divisor
        second_digit = divisor - remainder
        if second_digit < 2:
            second_digit = 0
        self.calculated_cpf = cpf_w_first_digit + str(second_digit)

    def validate_pattern(self):
        cpf_pattern = r"[\d]{3}.[\d]{3}.[\d]{3}-[\d]{2}"
        match_cpf = re.match(cpf_pattern, self.cpf)
        if match_cpf:
            return True
        return False

    def validate_digits(self):
        self.__remove_last_digits()
        self.__calculate_second_digit()

        if self.calculated_cpf == self.cpf:
            return True
        return False
