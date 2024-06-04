from pydantic import BaseModel


class ClientOutput(BaseModel):
    client_id: str
    name: str
    company_name: str
    cellphone: str
    cpf_cnpj: str
