import re

from src.clients.interfaces.i_validator import CPFCNPJValidatorInterface


class CNPJValidationService(CPFCNPJValidatorInterface):

    def __init__(self, cnpj_string: str):
        self.cnpj = cnpj_string
        self.calculated_cnpj = None
        self.__cnpj_no_digit = None

    def remove_dots_hyphen(self):
        no_dots_hyphen = re.sub(r"[.\-/]", "", self.cnpj)
        self.cnpj = no_dots_hyphen

    def remove_last_digits(self):
        self.remove_dots_hyphen()
        self.__cnpj_no_digit = self.cnpj[:-2]

    def calculate_first_digit(self):
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

    def calculate_second_digit(self):
        multiplier = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total_sum = 0
        divisor = 11

        cnpj_w_first_digit = self.__cnpj_no_digit + self.calculate_first_digit()
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
        self.remove_last_digits()
        self.calculate_second_digit()

        if self.calculated_cnpj == self.cnpj:
            return True
        return False
