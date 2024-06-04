from src.users.interfaces.i_user_validator import UserValidatorInterface


class UserValidationController:

    def __init__(self, validate: UserValidatorInterface):
        self.validate = validate

    def validate_user_data(self):
        return self.validate.validate_user_schema()
