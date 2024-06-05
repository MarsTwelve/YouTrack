import pytest
from hamcrest import assert_that, equal_to

from src.profiles.services.profile_validation import ProfileNameValidationService
from src.profiles.services.profile_validation import ProfileUpdateValidationService
from src.exeptions.custom_exeptions import BadRequestException


def test_profile_valid_name_validator(make_profile_schema):
    profile_pass = make_profile_schema()
    validate = ProfileNameValidationService(profile_pass.profile_name)
    assert_that(validate.validate_profile_name(), equal_to(True))


def test_profile_invalid_name_validator(make_profile_schema):
    profile_fail = make_profile_schema(profile_name=" Inv@lid pr#file n4me")
    validate = ProfileNameValidationService(profile_fail.profile_name)

    with pytest.raises(BadRequestException):
        validate.validate_profile_name()


def test_profile_valid_update_fields_validation(make_profile_update_schema):
    profile_pass = make_profile_update_schema()
    validate = ProfileUpdateValidationService(profile_pass)
    assert_that(validate.profile_update_field_validator(), equal_to(True))


def test_profile_invalid_update_fields_validation(make_profile_update_schema):
    profile_fail = make_profile_update_schema(update_field="non ecxiste")
    validate = ProfileUpdateValidationService(profile_fail)
    assert_that(validate.profile_update_field_validator(), equal_to(False))


def test_profile_valid_update_param_on_bool_fields_validation(make_profile_update_schema):
    profile_pass = make_profile_update_schema()
    validate = ProfileUpdateValidationService(profile_pass)
    assert_that(validate.profile_update_param_validator(), equal_to(True))


def test_profile_invalid_update_param_on_bool_fields_validation(make_profile_update_schema):
    profile_fail = make_profile_update_schema(update_param="False")
    validate = ProfileUpdateValidationService(profile_fail)
    assert_that(validate.profile_update_param_validator(), equal_to(False))


def test_profile_valid_update_param_on_profile_name_field_validation(make_profile_update_schema):
    profile_pass = make_profile_update_schema(update_field="profile_name",
                                              update_param="profile")
    validate = ProfileUpdateValidationService(profile_pass)
    assert_that(validate.profile_update_param_validator(), equal_to(False))


def test_profile_invalid_update_param_on_profile_name_field_validation(make_profile_update_schema):
    profile_fail = make_profile_update_schema(update_field="profile_name",
                                              update_param="Nome inv@lido")
    validate = ProfileUpdateValidationService(profile_fail)
    assert_that(validate.profile_update_param_validator(), equal_to(True))
