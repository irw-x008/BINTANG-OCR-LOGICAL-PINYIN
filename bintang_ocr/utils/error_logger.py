import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    logger = logging.getLogger("BintangOCR")
    logger.setLevel(logging.DEBUG)
    
    handler = RotatingFileHandler("logs/error.log", maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()

def log_error(msg):
    logger.error(msg)
    
def log_info(msg):
    logger.info(msg)
