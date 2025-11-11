from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from common.config import settings
from common.models.base import Base
from common.models.event import Event


engine = create_engine(settings.POSTGRES_DSN, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))


def init_db():
    Base.metadata.create_all(bind=engine)
