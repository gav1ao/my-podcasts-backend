from typing import List

from pydantic import BaseModel, RootModel

from model import Podcast
from schemas import ConflictErrorSchema


class PodcastSchema(BaseModel):
    """
    Entidade que representa um podcast.
    """

    id: int
    titulo: str
    descricao: str
    autor: str
    poster_url: str
    feed_url: str

    class Config:
        from_attributes = True

    @staticmethod
    def model_validate_many(podcasts: list[Podcast]) -> list:
        return [PodcastSchema.model_validate(p) for p in podcasts]

    @staticmethod
    def model_dump_many(podcasts: list[Podcast]) -> list:
        schemas = PodcastSchema.model_validate_many(podcasts)
        return [s.model_dump() for s in schemas]


class CadastroPodcastBodySchema(BaseModel):
    rss_feed_url: str


class PodcastBodySchema(BaseModel):
    """
    Identificador do podcast presente no body.
    """
    podcast_id: int


class PodcastPathSchema(PodcastBodySchema):
    """
    Identificador do podcast presente no path.
    """
    pass


class PodcastListSchema(RootModel[List[PodcastSchema]]):
    """
    Listagem de podcasts.
    """
    pass


class PodcastJaCadastradoSchema(ConflictErrorSchema):
    """
        Entidade que representa um podcast já cadastrado,
        """
    pass


class PodcastExistenteSchema(ConflictErrorSchema):
    """
    Entidade que representa um podcast já existente na lista do usuário.
    """
    pass


class PodcastExcluidoSchema(BaseModel):
    """
    Entidade que representa um podcast removido da lista do usuário com sucesso.
    """
    pass
