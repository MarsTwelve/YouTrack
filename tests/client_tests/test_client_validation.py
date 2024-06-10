from hamcrest import assert_that, equal_to

from src.clients.services.new_client_validation import ClientValidatorService
from src.clients.services.cpf_validation import CPFValidationService
from src.clients.services.cnpj_validation import CNPJValidationService


def test_format_spacing_validator(make_client_schema):
    client_bad = make_client_schema(name="        Standard      Name    ",
                                    company_name="     Standard       Company      Name      ",
                                    cellphone="         +55        (14)991031566         ",
                                    cpf_cnpj="                     464.085.468-46         ")
    client_good = make_client_schema()
    cpf_validation_service = CPFValidationService(client_bad.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client_bad.cpf_cnpj)
    validate = ClientValidatorService(client_bad, cpf_validation_service, cnpj_validation_service)
    assert_that(validate.format_spacing(), equal_to(client_good))


def test_client_validator_not_contains_invalid_chars(make_client_schema):
    client_pass = make_client_schema()
    cpf_validation_service = CPFValidationService(client_pass.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client_pass.cpf_cnpj)
    validate = ClientValidatorService(client_pass, cpf_validation_service, cnpj_validation_service)
    assert_that(validate.validate_invalid_chars(), equal_to(False))


def test_client_validator_contains_invalid_chars_name(make_client_schema):
    client_fail = make_client_schema(name="     Sta#%@ndard   co#%pany  name   ")
    cpf_validation_service = CPFValidationService(client_fail.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client_fail.cpf_cnpj)
    validate = ClientValidatorService(client_fail, cpf_validation_service, cnpj_validation_service)
    assert_that(validate.validate_invalid_chars(), equal_to(True))


def test_client_validator_contains_invalid_chars_company_name(make_client_schema):
    client_fail = make_client_schema(company_name="     Sta#%@ndard   co#%pany  name   ")
    cpf_validation_service = CPFValidationService(client_fail.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client_fail.cpf_cnpj)
    validate = ClientValidatorService(client_fail, cpf_validation_service, cnpj_validation_service)
    assert_that(validate.validate_invalid_chars(), equal_to(True))


def test_client_validator_correct_phone_pattern(make_client_schema):
    client_pass = make_client_schema()
    cpf_validation_service = CPFValidationService(client_pass.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client_pass.cpf_cnpj)
    validate = ClientValidatorService(client_pass, cpf_validation_service, cnpj_validation_service)
    assert_that(validate.validate_cellphone_pattern(), equal_to(True))


def test_client_validator_incorrect_phone_pattern_pass(make_client_schema):
    client_fail = make_client_schema(cellphone="+55 (16)555555559")
    cpf_validation_service = CPFValidationService(client_fail.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client_fail.cpf_cnpj)
    validate = ClientValidatorService(client_fail, cpf_validation_service, cnpj_validation_service)
    assert_that(validate.validate_cellphone_pattern(), equal_to(False))


def test_client_validator_validate_all_function_pass(make_client_schema):
    client = make_client_schema()
    cpf_validation_service = CPFValidationService(client.cpf_cnpj)
    cnpj_validation_service = CNPJValidationService(client.cpf_cnpj)
    validate = ClientValidatorService(client, cpf_validation_service, cnpj_validation_service)
    assert_that(validate.validate_new_client_schema(), equal_to(True))
