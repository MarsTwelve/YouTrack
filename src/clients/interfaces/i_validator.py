from abc import ABC, abstractmethod


class BaseClientValidationInterface(ABC):
    @abstractmethod
    def format_spacing(self):
        pass

    @abstractmethod
    def validate_invalid_chars(self):
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
    def validate_cpf(self):
        pass

    @abstractmethod
    def validate_cnpj(self):
        pass


class ClientUpdateValidationInterface(BaseClientValidationInterface, ABC):
    @abstractmethod
    def validate_update_field(self):
        pass

    @abstractmethod
    def validate_update_parameters(self):
        pass
