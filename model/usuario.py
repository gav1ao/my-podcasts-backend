from sqlalchemy import Column, String, PrimaryKeyConstraint, Integer

from model import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_usuario'),
    )

    def __init__(self, email: str, senha: str, nome: str):
        self.email = email
        self.senha = senha
        self.nome = nome
