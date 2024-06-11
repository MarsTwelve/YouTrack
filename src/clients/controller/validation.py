from src.clients.interfaces.i_validator import (NewClientValidationInterface,
                                                ClientNameValidationInterface,
                                                ClientUpdateValidationInterface)


class NewClientValidationController:

    def __init__(self, validate: NewClientValidationInterface):
        self.__validate = validate

    def validate_new_client(self):
        return self.__validate.validate_new_client_schema()


class ClientNameValidationController:
    def __init__(self, validate: ClientNameValidationInterface):
        self.__validate = validate

    def validate_client_name(self):
        return self.__validate.validate_name()


class ClientUpdateValidationController:

    def __init__(self, validate: ClientUpdateValidationInterface):
        self.__validate = validate

    def validate_client_update(self):
        return self.__validate.validate_update_field()
