import pytest
from hamcrest import assert_that, equal_to

from src.exeptions.custom_exeptions import BadRequestException

from src.users.services.user_validation import UserValidatorService
from src.users.services.user_validation import UserUpdateValidationService


def test_user_validator_format_user_schema_spacing(make_user_schema):
    user_bad = make_user_schema(username="          Standard          Username        ",
                                password="           P4ssW0rd_            ",
                                email="             standard.std@email.provider.com              ")
    user_good = make_user_schema()
    validate = UserValidatorService(user_bad)
    assert_that(validate.format_spacing(), equal_to(user_good))


def test_user_validator_contains_invalid_characters(make_user_schema):
    user_pass = make_user_schema()
    validate = UserValidatorService(user_pass)
    assert_that(validate.validate_invalid_chars(), equal_to(False))


def test_user_validator_validates_correct_email_format(make_user_schema):
    user_pass = make_user_schema()
    validate = UserValidatorService(user_pass)
    assert_that(validate.validate_email_format(), equal_to(True))


def test_user_validator_validates_correct_password_format(make_user_schema):
    user_pass = make_user_schema()
    validate = UserValidatorService(user_pass)
    assert_that(validate.validate_password_format(), equal_to(True))


def test_user_validator_validates_correct_language_selected(make_user_schema):
    user_options_pass = make_user_schema()
    validate = UserValidatorService(user_options_pass)
    assert_that(validate.validate_language(), equal_to(True))


def test_user_validator_validates_correct_currency_selected(make_user_schema):
    user_options_pass = make_user_schema()
    validate = UserValidatorService(user_options_pass)
    assert_that(validate.validate_currency(), equal_to(True))


def test_user_validator_validates_correct_country_selected(make_user_schema):
    user_options_pass = make_user_schema()
    validate = UserValidatorService(user_options_pass)
    assert_that(validate.validate_country(), equal_to(True))


def test_user_validator_validates_correct_speed_unit_selected(make_user_schema):
    user_options_pass = make_user_schema()
    validate = UserValidatorService(user_options_pass)
    assert_that(validate.validate_speed_unit(), equal_to(True))


def test_user_validator_validates_correct_volume_unit_selected(make_user_schema):
    user_options_pass = make_user_schema()
    validate = UserValidatorService(user_options_pass)
    assert_that(validate.validate_volume_unit(), equal_to(True))


def test_user_validator_validates_correct_length_unit_selected(make_user_schema):
    user_options_pass = make_user_schema()
    validate = UserValidatorService(user_options_pass)
    assert_that(validate.validate_length_unit(), equal_to(True))


def test_user_validator_validates_correct_temperature_unit_selected(make_user_schema):
    user_options_pass = make_user_schema()
    validate = UserValidatorService(user_options_pass)
    assert_that(validate.validate_temperature_unit(), equal_to(True))


def test_user_validator_validates_correct_user_main_function(make_user_schema):
    user_pass = make_user_schema()
    validate = UserValidatorService(user_pass)
    assert_that(validate.validate_user_schema(), equal_to(None))


def test_user_update_validator_correct_validate_user_schema(make_user_update_schema):
    user_update_pass = make_user_update_schema()
    validate = UserUpdateValidationService(user_update_pass)
    assert_that(validate.validate_user_schema(), equal_to(None))


def test_user_update_validator_incorrect_update_field(make_user_update_schema):
    user_update_fail = make_user_update_schema(update_field="non ecxiste")
    validate = UserUpdateValidationService(user_update_fail)
    with pytest.raises(BadRequestException):
        validate.validate_user_schema()


def test_user_update_validator_incorrect_update_param(make_user_update_schema):
    user_update_fail = make_user_update_schema(update_param="non ecxiste")
    validate = UserUpdateValidationService(user_update_fail)
    with pytest.raises(BadRequestException):
        validate.validate_user_schema()
