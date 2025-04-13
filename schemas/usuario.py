from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True


class UsuarioLoginFormSchema(BaseModel):
    """
    Define as informações necessárias para um usuário logar na aplicação.
    """
    email: str
    senha: str


class UsuarioFormSchema(BaseModel):
    """
    Define as informações necessárias para o cadastro de um novo usuário.
    """
    nome: str
    email: str
    senha: str
