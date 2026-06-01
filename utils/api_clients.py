import requests
import logging
logger = logging.getLogger()

def fetch_movies(url):
    logger.info("Fetching movies from OMBD API...")
    response = requests.get(url)
    json_data = response.json()
    movies_list = json_data.get("Search", [])
    return movies_list

def fetch_episodes(url):
    logger.info("Fetching episodes from Rick &n Morty API")
    response = requests.get(url)
    json_data = response.json()
    episodes_list = json_data.get("results", [])
    return episodes_list
