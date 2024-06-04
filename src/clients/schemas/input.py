from pydantic import BaseModel


class ClientInput(BaseModel):
    name: str
    company_name: str
    cellphone: str
    cpf_cnpj: str
