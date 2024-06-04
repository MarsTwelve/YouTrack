from hamcrest import assert_that, equal_to

from src.clients.services.new_client_validation import ClientValidatorService


def test_format_spacing_validator(make_client_schema):
    client_bad = make_client_schema(name="        Standard      Name    ",
                                    company_name="     Standard       Company      Name      ",
                                    cellphone="         +55        (14)991031566         ",
                                    cpf_cnpj="                     464.085.468-46         ")
    client_good = make_client_schema()
    validate = ClientValidatorService(client_bad)
    assert_that(validate.format_spacing(), equal_to(client_good))


def test_client_validator_not_contains_invalid_chars_pass(make_client_schema):
    client_pass = make_client_schema()
    validate = ClientValidatorService(client_pass)
    assert_that(validate.validate_invalid_chars(), equal_to(False))


def test_client_validator_contains_invalid_chars_name_pass(make_client_schema):
    client_fail = make_client_schema(name="     Sta#%@ndard   co#%pany  name   ")
    validate = ClientValidatorService(client_fail)
    assert_that(validate.validate_invalid_chars(), equal_to(True))


def test_client_validator_contains_invalid_chars_company_name_pass(make_client_schema):
    client_fail = make_client_schema(company_name="     Sta#%@ndard   co#%pany  name   ")
    validate = ClientValidatorService(client_fail)
    assert_that(validate.validate_invalid_chars(), equal_to(True))


def test_client_validator_correct_phone_pattern_pass(make_client_schema):
    client_pass = make_client_schema()
    validate = ClientValidatorService(client_pass)
    assert_that(validate.validate_cellphone_pattern(), equal_to(True))


def test_client_validator_incorrect_phone_pattern_pass(make_client_schema):
    client_fail = make_client_schema(cellphone="+55 (16)555555559")
    validate = ClientValidatorService(client_fail)
    assert_that(validate.validate_cellphone_pattern(), equal_to(False))


def test_client_validator_correct_cpf_pattern_pass(make_client_schema):
    client_pass = make_client_schema()
    validate = ClientValidatorService(client_pass)
    assert_that(validate.validate_cpf(), equal_to(True))


def test_client_validator_incorrect_cpf_pattern_pass(make_client_schema):
    client_fail = make_client_schema(cpf_cnpj="asdjialsfcjafsçoi")
    validate = ClientValidatorService(client_fail)
    assert_that(validate.validate_cpf(), equal_to(False))


def test_client_validator_validate_all_function_pass(make_client_schema):
    client = make_client_schema()
    validate = ClientValidatorService(client)
    assert_that(validate.is_valid(), equal_to(True))
