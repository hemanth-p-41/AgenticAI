import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(log_dir: str = None, level: int = logging.INFO):
    if log_dir is None:
        log_dir = os.getenv('LOG_DIR', '/app/logs')
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
    logger.addHandler(ch)

    # Rotating file handler
    fh = RotatingFileHandler(os.path.join(log_dir, 'app.log'), maxBytes=10 * 1024 * 1024, backupCount=5)
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
    logger.addHandler(fh)

    return logger
