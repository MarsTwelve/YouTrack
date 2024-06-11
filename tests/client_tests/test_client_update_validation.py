import pytest
from hamcrest import assert_that, equal_to

from src.clients.services.client_update_validation import ClientUpdateValidationService
from src.exeptions.custom_exeptions import BadRequestException


def test_client_update_validator_correct_client_update_schema(make_client_update_schema):
    client_update_pass = make_client_update_schema()
    validate = ClientUpdateValidationService(client_update_pass)
    assert_that(validate.validate_client_update_schema(), equal_to(None))


def test_client_update_validator_incorrect_update_field(make_client_update_schema):
    client_update_fail = make_client_update_schema(update_field="non ecxiste")
    validate = ClientUpdateValidationService(client_update_fail)
    with pytest.raises(BadRequestException):
        validate.validate_client_update_schema()


def test_client_update_validator_incorrect_update_param_cellphone(make_client_update_schema):
    client_update_fail = make_client_update_schema(update_field="cellphone",
                                                   update_param="non ecxiste")
    validate = ClientUpdateValidationService(client_update_fail)
    with pytest.raises(BadRequestException):
        validate.validate_client_update_schema()


def test_client_update_validator_correct_update_param_cellphone(make_client_update_schema):
    client_update_fail = make_client_update_schema(update_field="cellphone",
                                                   update_param="+55 (14)991031566")
    validate = ClientUpdateValidationService(client_update_fail)
    assert_that(validate.validate_client_update_schema(), equal_to(None))
