import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Sets up the logging configuration."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set to INFO or ERROR for production

    # Create a file handler which logs even debug messages
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(handler)

    # StreamHandler to output logs to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
