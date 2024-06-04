import pytest
from hamcrest import assert_that, equal_to

from src.vehicles.services.validation import VehicleValidationService


def test_format_spacing_validator(make_vehicle_schema):
    vehicle_bad = make_vehicle_schema(vehicle_make="         Standard      Vehicle        Brand       ",
                                      vehicle_model="       Standard      Vehicle        Model       ",
                                      vehicle_trim="       Standard      Vehicle        Trim        ",
                                      vehicle_color="     Standard      Vehicle        Color       ",
                                      manufacture_year=2024,
                                      number_plate="     AWS3F98                                  ")
    vehicle_good = make_vehicle_schema()
    validate = VehicleValidationService(vehicle_bad)
    assert_that(validate.format_spacing(), equal_to(vehicle_good))


def test_vehicle_validator_contains_valid_characters_pass(make_vehicle_schema):
    vehicle = make_vehicle_schema()
    validate = VehicleValidationService(vehicle)
    assert_that(validate.validate_invalid_chars(), equal_to(False))


def test_vehicle_validator_valid_number_plate_pattern_pass(make_vehicle_schema):
    vehicle = make_vehicle_schema()
    validate = VehicleValidationService(vehicle)
    assert_that(validate.validate_plate_format(), equal_to(True))


def test_vehicle_validator_validate_valid_manufacture_year_pass(make_vehicle_schema):
    vehicle = make_vehicle_schema()
    validate = VehicleValidationService(vehicle)
    assert_that(validate.validate_manufacture_year(), equal_to(True))


def test_vehicle_validator_contains_invalid_characters_pass(make_vehicle_schema):
    vehicle = make_vehicle_schema(vehicle_color="Cor aleat$ria")
    validate = VehicleValidationService(vehicle)
    assert_that(validate.validate_invalid_chars(), equal_to(True))


def test_vehicle_validator_validate_invalid_manufacture_year_pass(make_vehicle_schema):
    vehicle = make_vehicle_schema(manufacture_year=2025)
    validate = VehicleValidationService(vehicle)
    assert_that(validate.validate_manufacture_year(), equal_to(False))


def test_vehicle_validator_invalid_number_plate_pattern_pass(make_vehicle_schema):
    vehicle = make_vehicle_schema(number_plate="AAA7568")
    validate = VehicleValidationService(vehicle)
    assert_that(validate.validate_plate_format(), equal_to(False))
