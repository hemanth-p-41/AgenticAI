import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os


def setup_logging(log_dir: str = None, level: int = logging.INFO):
    """
    Configure logging for both local development and Render deployment.
    Logs are stored in a project-relative 'logs' directory if possible.
    If file logging cannot be initialized, the application falls back to
    console logging only.
    """

    if log_dir is None:
        log_dir = os.getenv("LOG_DIR", "logs")

    log_path = Path(log_dir)

    logger = logging.getLogger()

    # Prevent duplicate handlers after reloads
    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    # Console logging (always enabled)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File logging (optional)
    try:
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_path / "app.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
        )

        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except Exception as e:
        logger.warning(f"File logging disabled: {e}")

    return logger