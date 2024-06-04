from hamcrest import assert_that, equal_to

from src.clients.services.new_client_validation import CNPJValidator


def test_cnpj_validator_valid_cnpj_digits_pass(make_client_schema):
    client_pass = make_client_schema(cpf_cnpj="11.222.333/0001-81")
    validate = CNPJValidator(client_pass.cpf_cnpj)
    assert_that(validate.validate_digits(), equal_to(True))


def test_cnpj_validator_invalid_cnpj_digits_pass(make_client_schema):
    client_pass = make_client_schema(cpf_cnpj="11.222.333/0001-56")
    validate = CNPJValidator(client_pass.cpf_cnpj)
    assert_that(validate.validate_digits(), equal_to(False))
