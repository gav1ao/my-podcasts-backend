import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from model.base import Base
from model.podcast import Podcast
from model.rel_podcast_usuario import RelPodcastUsuario
from model.usuario import Usuario

db_path = "database/"

if not os.path.exists(db_path):
    os.makedirs(db_path)

DATABASE_URL = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)
