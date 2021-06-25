import logging

logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s")


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger
