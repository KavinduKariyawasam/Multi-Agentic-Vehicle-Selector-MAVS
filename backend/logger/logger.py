import logging
import sys

# Create a custom logger
logger = logging.getLogger("vehicle_recommender")

# Avoid adding handlers multiple times if logger.py is imported in many files
if not logger.handlers:
    # Configure the logger
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Default logging level
    logger.setLevel(logging.INFO)

# Optional helper for other modules
def set_log_level(level: int):
    """Dynamically update the logger's level."""
    logger.setLevel(level)
