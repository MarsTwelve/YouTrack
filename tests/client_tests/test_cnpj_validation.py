from hamcrest import assert_that, equal_to

from src.clients.services.cnpj_validation import CNPJValidationService


def test_cnpj_validator_valid_cnpj_digits(make_client_schema):
    client_pass = make_client_schema(cpf_cnpj="11.222.333/0001-81")
    validate = CNPJValidationService(client_pass.cpf_cnpj)
    assert_that(validate.validate_digits(), equal_to(True))


def test_cnpj_validator_invalid_cnpj_digits(make_client_schema):
    client_fail = make_client_schema(cpf_cnpj="11.222.333/0001-56")
    validate = CNPJValidationService(client_fail.cpf_cnpj)
    assert_that(validate.validate_digits(), equal_to(False))


def test_cnpj_validator_invalid_cnpj_pattern(make_client_schema):
    client_fail = make_client_schema(cpf_cnpj="111.222.333/12222-87")
    validate = CNPJValidationService(client_fail.cpf_cnpj)
    assert_that(validate.validate_pattern(), equal_to(False))
