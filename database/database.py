from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings.config import settings
import logging


LOGGER = logging.getLogger(__name__)
SQLALCHEMY_DATABASE_URL = settings.sql_alchemy_database_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL, **settings.sql_alchemy_engine_options())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    LOGGER.info(f"Current Connection Pool Number: {engine.pool.checkedout()}")
    try:
        yield db
    finally:
        db.close()