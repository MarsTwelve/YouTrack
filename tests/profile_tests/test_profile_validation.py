import pytest
from hamcrest import assert_that, equal_to, is_, none

from src.profiles.services.profile_validation import ProfileNameValidationService
from src.profiles.services.profile_validation import ProfileUpdateValidationService
from src.exeptions.custom_exeptions import BadRequestException


def test_profile_valid_name_validator_pass(make_profile_schema):
    profile_pass = make_profile_schema()
    validate = ProfileNameValidationService(profile_pass.profile_name)
    assert_that(validate.validate_profile_name(), is_(none()))


def test_profile_invalid_name_validator_pass(make_profile_schema):
    profile_fail = make_profile_schema(profile_name=" Inv@lid pr#file n4me")
    validate = ProfileNameValidationService(profile_fail.profile_name)

    with pytest.raises(BadRequestException):
        validate.validate_profile_name()


def test_profile_valid_update_fields_validation_pass(make_profile_update_schema):
    profile_pass = make_profile_update_schema()
    validate = ProfileUpdateValidationService(profile_pass)
    assert_that(validate.profile_update_field_validator(), is_(none()))


def test_profile_invalid_update_fields_validation_pass(make_profile_update_schema):
    profile_fail = make_profile_update_schema(update_field="non ecxiste")
    validate = ProfileUpdateValidationService(profile_fail)
    assert_that(validate.profile_update_field_validator(), equal_to(False))
