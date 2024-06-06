from abc import ABC, abstractmethod


class UserBaseValidatorInterface(ABC):
    @abstractmethod
    def format_spacing(self):
        pass

    @abstractmethod
    def validate_invalid_chars(self):
        pass


class UserValidatorInterface(UserBaseValidatorInterface):

    @abstractmethod
    def validate_email_format(self):
        pass

    @abstractmethod
    def validate_password_format(self):
        pass

    @abstractmethod
    def validate_language(self):
        pass

    @abstractmethod
    def validate_currency(self):
        pass

    @abstractmethod
    def validate_country(self):
        pass

    @abstractmethod
    def validate_speed_unit(self):
        pass

    @abstractmethod
    def validate_volume_unit(self):
        pass

    @abstractmethod
    def validate_length_unit(self):
        pass

    @abstractmethod
    def validate_temperature_unit(self):
        pass

    @abstractmethod
    def validate_user_schema(self):
        pass
