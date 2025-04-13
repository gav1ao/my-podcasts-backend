import logging

import feedparser
from feedparser import FeedParserDict
from flask import jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_refresh_token
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy import select, func
from werkzeug.exceptions import Conflict, HTTPException, abort, NotFound, BadRequest, Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash

from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES
from logger import setup as settup_logging
from model import Session, Usuario, RelPodcastUsuario
from schemas import *

settup_logging()

jwt = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
}
security_schemes = {"jwt": jwt}

security = [{"jwt": []}]
info = Info(title="Meus Podcasts API", version="1.0.0", security_schemes=security_schemes)
app = OpenAPI(__name__, info=info)
CORS(app)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = JWT_REFRESH_TOKEN_EXPIRES

jwt = JWTManager(app)

log = logging.getLogger(__name__)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

auth_tag = Tag(name="Autenticação", description="Rotas relacionadas com a autenticação à plataforma")
usuario_tag = Tag(name="Usuário",
                  description="Criação de usuários e rotas específicas para manipulação de dados do usuário")
podcast_tag = Tag(name="Podcast", description="Adição, visualização e remoção de podcasts à base")


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Retorna JSON ao invés de HTML para erros HTTP padrão (ex: 409, 404)."""
    response = e.get_response()
    response.data = jsonify({
        "error": e.name,
        "message": e.description,
        "status_code": e.code
    }).data
    response.content_type = "application/json"
    log.error(e)
    return response


@app.errorhandler(Exception)
def handle_generic_exception(e):
    return jsonify({
        "error": "Internal Server Error",
        "message": str(e),
        "status_code": 500
    }), 500


@app.get("/", tags=[home_tag])
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect("/openapi")


@app.post("/usuario",
          tags=[usuario_tag],
          responses={201: UsuarioSchema, 400: BadRequestErrorSchema, 500: InternalServerErrorSchema})
def criar_usuario(body: UsuarioFormSchema):
    """
    Permite efetuar a criação de um novo usuário.

    Retorna o usuário criado.
    """

    nome: str = body.nome
    email: str = body.email
    senha: str = body.senha

    session = Session()
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if usuario:
        raise BadRequest(f"E-mail {email} já cadastrado.")

    senha_hash = generate_password_hash(senha)
    usuario = Usuario(email, senha_hash, nome)

    try:
        session.add(usuario)
        session.commit()

        usuario = session.query(Usuario).filter(Usuario.email == email).first()

        usuario_schema = UsuarioSchema.model_validate(usuario).model_dump()

        return usuario_schema, 201
    except Exception as ex:
        msg = "Ocorreu um erro inesperado ao criar usuário."
        log.exception(msg)

        abort(500, msg)


@app.post("/login",
          tags=[auth_tag],
          responses={200: TokenSchema, 400: BadRequestErrorSchema, 401: UnauthorizedErrorSchema,
                     500: InternalServerErrorSchema})
def login(body: UsuarioLoginFormSchema):
    """
    Permite efetuar o login do usuário.

    Efetua o login do usuário e retorna um token de acesso e um token de refresh.
    """

    email = body.email
    senha = body.senha

    if not email or not senha:
        raise BadRequest("Email e/ou senha não preenchidos.")

    session = Session()
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    senha_valida = check_password_hash(usuario.senha, senha) if usuario else False

    if not usuario or not senha_valida:
        raise Unauthorized("Email e/ou senha inválidos.")

    usuario_id = str(usuario.id)
    access_token = create_access_token(identity=usuario_id,
                                       additional_claims={
                                           "nome": usuario.nome,
                                           "email": usuario.email
                                       })
    refresh_token = create_refresh_token(identity=usuario_id)

    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.post("/refresh",
          tags=[auth_tag],
          security=security,
          responses={200: AccessTokenSchema, 401: UnauthorizedErrorSchema, 500: InternalServerErrorSchema})
@jwt_required(refresh=True)
def refresh():
    """
    Permite efetuar o refresh do token de acesso.

    Retorna um novo token de acesso.
    """

    usuario_id = get_jwt_identity()
    access_token = create_access_token(identity=usuario_id)

    return jsonify(access_token=access_token)


@app.get("/podcast",
         tags=[podcast_tag],
         responses={200: PodcastListSchema, 500: InternalServerErrorSchema})
def obter_podcasts():
    """
    Permite obter todos os podcasts cadastrados na base de dados.

    Retorna uma lista de podcasts.
    """
    session = Session()
    podcasts = session.scalars(select(Podcast)).all()

    return jsonify(PodcastSchema.model_dump_many(podcasts))


@app.get("/podcast/<int:podcast_id>",
         tags=[podcast_tag],
         responses={200: PodcastSchema, 500: InternalServerErrorSchema})
def obter_podcast(path: PodcastPathSchema):
    """
    Obtém as informações de um podcast específico.

    Retorna o podcast encontrado.
    """

    podcast_id: int = path.podcast_id

    log.info(f"Buscando podcast de id [{podcast_id}]")

    session = Session()
    podcast = session.query(Podcast).filter(Podcast.id == podcast_id).first()

    if not podcast:
        msg = f"Podcast de id [{podcast_id}] não encontrado."
        log.warning(msg)

        raise NotFound(msg)

    schema = PodcastSchema.model_validate(podcast)

    return PodcastSchema.model_dump(schema), 200


@app.post("/podcast/importar",
          tags=[podcast_tag],
          responses={200: PodcastSchema, 409: PodcastJaCadastradoSchema, 500: InternalServerErrorSchema})
def importar_podcast(body: CadastroPodcastBodySchema):
    """
    A partir da URL do feed, importa o podcast para a base de dados.

    Retorna o podcast cadastrado.
    """
    feed_url: str = body.rss_feed_url
    try:
        dados: FeedParserDict = feedparser.parse(feed_url)
    except Exception as ex:
        msg = "Ocorreu um erro inesperado ao processar o feed."
        log.exception(msg)

        abort(500, msg)

    feed = dados.feed

    titulo = feed.title

    session = Session()
    podcast = session.query(Podcast).where(func.lower(Podcast.titulo) == func.lower(titulo)).first()

    if podcast:
        raise Conflict(description=f"Podcast '{titulo}' já cadastrado na plataforma.")

    descricao = feed.summary
    autor = feed.author_detail.name
    poster_url = feed.image.href

    try:
        podcast = Podcast(titulo=titulo, descricao=descricao, autor=autor, poster_url=poster_url, feed_url=feed_url)

        session.add(podcast)
        session.commit()

        podcast = session.query(Podcast).filter(Podcast.titulo == titulo).first()

        return jsonify(PodcastSchema.model_validate(podcast).model_dump())

    except Exception as e:
        msg = "Ocorreu um erro inesperado ao importar o podcast."
        log.exception(msg)

        abort(500, msg)


@app.get("/usuario/podcast",
         tags=[podcast_tag, usuario_tag],
         security=security,
         responses={200: PodcastListSchema, 500: InternalServerErrorSchema})
@jwt_required()
def obter_podcasts_usuario():
    """
    Obtêm as informações de todos os podcasts cadastrados na lista do usuário.

    Retorna uma lista de podcasts presentes na lista do usuário.
    """

    usuario_id = get_jwt_identity()

    session = Session()

    podcasts = (
        session
        .query(Podcast)
        .join(RelPodcastUsuario)
        .join(Usuario)
        .filter(Usuario.id == usuario_id)
        .all()
    )

    return PodcastSchema.model_dump_many(podcasts)


@app.post("/usuario/podcast",
          tags=[podcast_tag, usuario_tag],
          security=security,
          responses={201: PodcastSchema, 400: BadRequestErrorSchema, 404: NotFoundErrorSchema,
                     409: PodcastExistenteSchema, 500: InternalServerErrorSchema})
@jwt_required()
def adicionar_podcast(body: PodcastBodySchema):
    """
    Adiciona o podcast à lista do usuário.

    Retorna o podcast adicionado.
    """

    usuario_id = get_jwt_identity()

    podcast_id: int = body.podcast_id

    if not podcast_id:
        msg = "Atributo [podcast_id] é um campo obrigatório."
        log.warning(msg)

        raise BadRequest(msg)

    session = Session()
    podcast = session.query(Podcast).filter(Podcast.id == podcast_id).first()

    if not podcast:
        msg = f"Podcast de id [{podcast_id}] não encontrado."
        log.warning(msg)

        raise NotFound(msg)

    rel_podcast_usuario = (
        session
        .query(Podcast)
        .join(RelPodcastUsuario)
        .join(Usuario)
        .filter(Usuario.id == usuario_id)
        .filter(Podcast.id == podcast_id)
        .first()
    )

    if rel_podcast_usuario:
        raise Conflict(description="Podcast já cadastrado a lista do usuário.")

    rel_podcast_usuario = RelPodcastUsuario(usuario_id=usuario_id, podcast_id=podcast.id)

    try:
        session.add(rel_podcast_usuario)
        session.commit()

        podcast_schema = PodcastSchema.model_validate(podcast).model_dump()

        return podcast_schema, 201
    except Exception as ex:
        msg = "Ocorreu um erro inesperado ao adicionar podcast."
        log.exception(msg)

        abort(500, msg)


@app.delete("/usuario/podcast/<int:podcast_id>",
            tags=[podcast_tag, usuario_tag],
            security=security,
            responses={200: PodcastExcluidoSchema, 400: BadRequestErrorSchema, 404: NotFoundErrorSchema,
                       500: InternalServerErrorSchema})
@jwt_required()
def remover_podcast(path: PodcastPathSchema):
    """
    Remove um podcast da lista do usuário.
    """

    usuario_id = get_jwt_identity()

    podcast_id: int = path.podcast_id

    if not podcast_id:
        msg = "Atributo [podcast_id] é um campo obrigatório."
        log.warning(msg)

        raise BadRequest(msg)

    session = Session()
    podcast = session.query(Podcast).filter(Podcast.id == podcast_id).first()

    if not podcast:
        msg = f"Podcast de id [{podcast_id}] não encontrado."
        log.warning(msg)

        raise NotFound(msg)

    rel_podcast_usuario = (
        session
        .query(RelPodcastUsuario)
        .join(Podcast)
        .join(Usuario)
        .filter(Usuario.id == usuario_id)
        .filter(Podcast.id == podcast_id)
        .first()
    )

    if not rel_podcast_usuario:
        raise NotFound(description="Podcast não encontrado na lista do usuário.")

    try:
        session.delete(rel_podcast_usuario)
        session.commit()

        return jsonify(message="Podcast removido da lista do usuário com sucesso."), 200
    except Exception as ex:
        msg = "Ocorreu um erro inesperado ao remover podcast."
        log.exception(msg)

        abort(500, msg)


if __name__ == "__main__":
    app.run(port=8080)
