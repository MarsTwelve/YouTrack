from hamcrest import assert_that, equal_to

from src.users.services.validation import UserValidatorService


def test_user_validator_format_user_schema_spacing(make_user_schema):
    user_bad = make_user_schema(username="          Standard          Username        ",
                                password="           P4ssW0rd_            ",
                                email="             standard.std@email.provider.com              ")
    user_good = make_user_schema()
    validate = UserValidatorService(user_bad)
    assert_that(validate.format_spacing(), equal_to(user_good))


def test_user_validator_contains_invalid_characters_pass(make_user_schema):
    user = make_user_schema()
    validate = UserValidatorService(user)
    assert_that(validate.validate_invalid_chars(), equal_to(False))


def test_user_validator_validates_email_format_pass(make_user_schema):
    user = make_user_schema()
    validate = UserValidatorService(user)
    assert_that(validate.validate_email_format(), equal_to(True))


def test_user_validator_validates_password_format_pass(make_user_schema):
    user = make_user_schema()
    validate = UserValidatorService(user)
    assert_that(validate.validate_password_format(), equal_to(True))


def test_user_validator_validates_language_selected_pass(make_user_schema):
    user_options = make_user_schema()
    validate = UserValidatorService(user_options)
    assert_that(validate.validate_language(), equal_to(True))


def test_user_validator_validates_currency_selected_pass(make_user_schema):
    user_options = make_user_schema()
    validate = UserValidatorService(user_options)
    assert_that(validate.validate_currency(), equal_to(True))


def test_user_validator_validates_country_selected_pass(make_user_schema):
    user_options = make_user_schema()
    validate = UserValidatorService(user_options)
    assert_that(validate.validate_country(), equal_to(True))


def test_user_validator_validates_speed_unit_selected_pass(make_user_schema):
    user_options = make_user_schema()
    validate = UserValidatorService(user_options)
    assert_that(validate.validate_speed_unit(), equal_to(True))


def test_user_validator_validates_volume_unit_selected_pass(make_user_schema):
    user_options = make_user_schema()
    validate = UserValidatorService(user_options)
    assert_that(validate.validate_volume_unit(), equal_to(True))


def test_user_validator_validates_length_unit_selected_pass(make_user_schema):
    user_options = make_user_schema()
    validate = UserValidatorService(user_options)
    assert_that(validate.validate_length_unit(), equal_to(True))


def test_user_validator_validates_temperature_unit_selected_pass(make_user_schema):
    user_options = make_user_schema()
    validate = UserValidatorService(user_options)
    assert_that(validate.validate_temperature_unit(), equal_to(True))


def test_user_validator_validates_user_validation_main_function_pass(make_user_schema):
    user = make_user_schema()
    validate = UserValidatorService(user)
    assert_that(validate.validate_user_schema(), equal_to(True))
