from hamcrest import assert_that, equal_to

from src.clients.services.cpf_validation import CPFValidationService


def test_cpf_validator_valid_cpf_digits_pass(make_client_schema):
    client_pass = make_client_schema()
    validate = CPFValidationService(client_pass.cpf_cnpj)
    assert_that(validate.validate_digits(), equal_to(True))


def test_cpf_validator_invalid_cpf_digits_pass(make_client_schema):
    client_fail = make_client_schema(cpf_cnpj="123.456.789-10")
    validate = CPFValidationService(client_fail.cpf_cnpj)
    assert_that(validate.validate_digits(), equal_to(False))


def test_cnpj_validator_invalid_cpf_pattern(make_client_schema):
    client_fail = make_client_schema(cpf_cnpj="555.555.7895-98")
    validate = CPFValidationService(client_fail.cpf_cnpj)
    assert_that(validate.validate_pattern(), equal_to(False))
