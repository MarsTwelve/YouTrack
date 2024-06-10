from abc import ABC, abstractmethod


class BaseClientValidationInterface(ABC):
    @abstractmethod
    def format_spacing(self):
        pass

    @abstractmethod
    def validate_invalid_chars(self):
        pass


class CPFCNPJValidatorInterface(ABC):
    @abstractmethod
    def remove_dots_hyphen(self):
        pass

    @abstractmethod
    def remove_last_digits(self):
        pass

    @abstractmethod
    def calculate_first_digit(self):
        pass

    @abstractmethod
    def calculate_second_digit(self):
        pass

    @abstractmethod
    def validate_pattern(self):
        pass

    @abstractmethod
    def validate_digits(self):
        pass


class ClientNameValidationInterface(BaseClientValidationInterface, ABC):
    @abstractmethod
    def validate_name(self):
        pass


class NewClientValidationInterface(BaseClientValidationInterface, ABC):
    @abstractmethod
    def validate_cellphone_pattern(self):
        pass

    @abstractmethod
    def validate_new_client_schema(self):
        pass


class ClientUpdateValidationInterface(BaseClientValidationInterface, ABC):
    @abstractmethod
    def validate_update_field(self):
        pass

    @abstractmethod
    def validate_update_parameters(self):
        pass
