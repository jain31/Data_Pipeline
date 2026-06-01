import os
import logging
from dotenv import load_dotenv
from config.logging_config import setup_logging
from utils.api_clients import fetch_movies, fetch_episodes
from utils.db_connector import get_db_session, OMDBMovie, RickMortyEpisode

def main():
    # 1. Secure absolute path for configuration file loading
    current_folder = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_folder, ".env")
    load_dotenv(dotenv_path=env_path)
    
    # 2. Start logging system
    setup_logging()
    logger = logging.getLogger()
    
    logger.info("================ STARTING DATA PIPELINE ================")
    
    # 3. Pull settings from system
    url_one = os.getenv("API_URL_ONE")
    url_two = os.getenv("API_URL_TWO")
    
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    # Check if .env was loaded successfully
    if not db_host or db_host == "None":
        logger.error(f"CRITICAL ERROR: Could not read .env details at path: {env_path}")
        logger.error("Please ensure your file is named exactly '.env' and placed in the project folder.")
        return

    # 4. Open up your database connection workspace
    session = get_db_session(db_user, db_pass, db_host, db_port, db_name)
    
    try:
        # 5. Extract and add Movie Records
        movies = fetch_movies(url_one)
        for item in movies:
            movie_record = OMDBMovie(
                title=item.get("Title"),
                year=item.get("Year"),
                imdb_id=item.get("imdbID")
            )
            session.add(movie_record) 
            
        # 6. Extract and add Episode Records
        episodes = fetch_episodes(url_two)
        for item in episodes:
            episode_record = RickMortyEpisode(
                name=item.get("name"),
                air_date=item.get("air_date"),
                episode_code=item.get("episode")
            )
            session.add(episode_record) 
            
        # 7. Final push to commit adjustments inside MySQL Workbench
        session.commit()
        logger.info("================ PIPELINE COMPLETED SUCCESSFULLY ================")
        
    except Exception as e:
        session.rollback() 
        logger.error(f"Pipeline encountered an error during data processing: {e}")
        
    finally:
        session.close() 

if __name__ == "__main__":
    main()