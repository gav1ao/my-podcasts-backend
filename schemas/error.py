from pydantic import BaseModel


class HttpExceptionSchema(BaseModel):
    """
    Entidade base para as exceções HTTP genéricas ou herdadas de HTTPException da biblioteca Werkzeug.
    """

    error: str
    message: str
    status_code: int


class InternalServerErrorSchema(HttpExceptionSchema):
    """
    Entidade utilizada para apresentação de erros inesperados ocorridos na servidor.
    """


class NotFoundErrorSchema(HttpExceptionSchema):
    """
    Entidade utilizada para quando um objeto não é encontrado.
    """


class ConflictErrorSchema(HttpExceptionSchema):
    """
    Entidade utilizada para representar quando um objeto sendo inserido já existe na base.
    """


class BadRequestErrorSchema(HttpExceptionSchema):
    """
    Atributo obrigatório inválido ou não informado.
    """


class UnauthorizedErrorSchema(HttpExceptionSchema):
    """
    Acesso não autorizado.
    """
