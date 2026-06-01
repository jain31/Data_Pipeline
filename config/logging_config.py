import logging 
import os
def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level = logging.INFO,
        format = log_format,
        handlers=[
            logging.FileHandler("logs/pipeline.log"),
            logging.StreamHandler()
        ]
    )