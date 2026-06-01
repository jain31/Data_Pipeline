import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger()
Base = declarative_base()

class OMDBMovie(Base):
    __tablename__ = 'omdb_movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    year = Column(String(50))
    imdb_id = Column(String(50))

class RickMortyEpisode(Base):
    __tablename__ = 'rick_morty_episodes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    air_date = Column(String(100))
    episode_code = Column(String(50))

def get_db_session(user, password, host, port, db_name):
    if not port or port == "None":
        port = "3306"
        
    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(db_url)
    
    # Builds tables in MySQL Workbench automatically
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    return Session()