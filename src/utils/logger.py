from pathlib import Path
from datetime import datetime
import logging


def setup_logging(log_dir):
    """Setup logging for system reports generation"""
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = (
        log_dir / f"system_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    # Create logger
    logger = logging.getLogger("system_reports")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    # Create formatters
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
