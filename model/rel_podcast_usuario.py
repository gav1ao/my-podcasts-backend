from sqlalchemy import Column, ForeignKey, Integer

from model import Base


class RelPodcastUsuario(Base):
    __tablename__ = "rel_podcast_usuario"

    usuario_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    podcast_id = Column(Integer, ForeignKey("podcast.id"), primary_key=True)
