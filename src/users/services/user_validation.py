import re
from abc import ABC

from src.users.interfaces.i_user_validation import UserValidatorInterface
from src.exeptions.custom_exeptions import BadRequestException


class UserValidatorService(UserValidatorInterface, ABC):

    def __init__(self, user_data):
        self.__user = user_data

    def format_spacing(self):
        for field_name, field_value in self.__user:
            truncate_spaces = re.sub(r"^\s+|\s+$", "", field_value)
            validated_string = re.sub(r"\s{2,}", " ", truncate_spaces)
            setattr(self.__user, field_name, validated_string)
        return self.__user

    def validate_invalid_chars(self):
        invalid_chars_pattern = r"[^A-z\s]"

        for field_name, field_value in self.__user:
            if field_name == "email" or field_name == "password" or field_name == "client_id":
                continue
            search = re.search(invalid_chars_pattern, field_value)
            print(field_name)
            if search:
                return True
        return False

    def validate_email_format(self):
        email_pattern = (r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*["
                         r"a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
        email_match = re.match(email_pattern, self.__user.email)
        if email_match:
            return True
        return False

    def validate_password_format(self):
        password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,64}$"
        password_match = re.match(password_pattern, self.__user.password)
        if password_match:
            return True
        return False

    def validate_language(self):
        accepted_languages = ["Portuguese", "Spanish", "English"]
        if self.__user.language in accepted_languages:
            return True
        return False

    def validate_currency(self):
        accepted_currencies = ["BRL", "COP", "CHP", "ARS", "UYU"]
        if self.__user.currency in accepted_currencies:
            return True
        return False

    def validate_country(self):
        accepted_countries = ["Brazil", "Colombia", "Bolivia", "Uruguay", "Argentina"]
        if self.__user.country in accepted_countries:
            return True
        return False

    def validate_speed_unit(self):
        accepted_units = ["KMH", "MPH"]
        if self.__user.unit_speed in accepted_units:
            return True
        return False

    def validate_volume_unit(self):
        accepted_units = ["Liter", "US Gallon"]
        if self.__user.unit_volume not in accepted_units:
            return False
        return True

    def validate_length_unit(self):
        accepted_units = ["Kilometer", "Mile"]
        if self.__user.unit_length not in accepted_units:
            return False
        return True

    def validate_temperature_unit(self):
        accepted_units = ["Celsius", "Fahrenheit"]
        if self.__user.unit_temp not in accepted_units:
            return False
        return True

    def validate_user_schema(self):
        base_response = "[ERR]VALIDATION_FAILED"
        self.format_spacing()
        if self.validate_invalid_chars():
            raise BadRequestException(base_response + " - Special characters and digits are not allowed here")

        if not self.validate_email_format():
            raise BadRequestException(base_response + " - Invalid Email Format")

        if not self.validate_password_format():
            raise BadRequestException(base_response + " - The password is too weak")

        if not self.validate_language():
            raise BadRequestException(base_response + " - This language is not supported")

        if not self.validate_currency():
            raise BadRequestException(base_response + " - This currency is not supported")

        if not self.validate_country():
            raise BadRequestException(base_response + " - This country is not available")

        if not self.validate_speed_unit():
            raise BadRequestException(base_response + " - Invalid speed unit type")

        if not self.validate_volume_unit():
            raise BadRequestException(base_response + " - Invalid volume unit type")

        if not self.validate_length_unit():
            raise BadRequestException(base_response + " - Invalid length unit type")

        if not self.validate_temperature_unit():
            raise BadRequestException(base_response + " - Invalid temperature unit type")
