import re

from src.clients.interfaces.i_validator import CPFCNPJValidatorInterface


class CPFValidationService(CPFCNPJValidatorInterface):

    def __init__(self, cpf_string: str):
        self.cpf = cpf_string
        self.calculated_cpf = None
        self.__cpf_no_digit = None

    def remove_dots_hyphen(self):
        no_dots_hyphen = re.sub(r"[.-]", "", self.cpf)
        self.cpf = no_dots_hyphen

    def remove_last_digits(self):
        self.remove_dots_hyphen()
        self.__cpf_no_digit = self.cpf[:-2]

    def calculate_first_digit(self):
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

    def calculate_second_digit(self):
        multiplier = 11
        total_sum = 0
        divisor = 11

        cpf_w_first_digit = self.__cpf_no_digit + self.calculate_first_digit()
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
        self.remove_last_digits()
        self.calculate_second_digit()

        if self.calculated_cpf == self.cpf:
            return True
        return False
