from sqlalchemy import Column, String, PrimaryKeyConstraint, Integer

from model import Base


class Podcast(Base):
    __tablename__ = "podcast"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), unique=True, nullable=False)
    descricao = Column(String(255))
    autor = Column(String(100), nullable=False)
    poster_url = Column(String(255))
    feed_url = Column(String(255), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_podcast'),
    )
