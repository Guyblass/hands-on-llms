import logging
import logging.config
import os
import yaml

from dotenv import load_dotenv, find_dotenv
from pathlib import Path


logger = logging.getLogger(__name__)



def run_immediately_decorator(func):
    func()

    return func


def initialize_logger(
    config_path: str = "logging.yaml", logs_dir_name: str = "logs"
) -> logging.Logger:
    """Initialize logger from a YAML config file."""

    # Create logs directory.
    config_path_parent = Path(config_path).parent
    logs_dir = config_path_parent / logs_dir_name
    logs_dir.mkdir(parents=True, exist_ok=True)

    with open(config_path, "rt") as f:
        config = yaml.safe_load(f.read())

    # Make sure that existing logger will still work.
    config["disable_existing_loggers"] = False

    logging.config.dictConfig(config)


@run_immediately_decorator
def initialize(logging_config_path: str = os.path.join("..", "logging.yaml")):
     # Initialize logger.
    try:
        initialize_logger(config_path=logging_config_path)
    except FileNotFoundError:
        logger.warning(f"No logging configuration file found at: {logging_config_path}. Setting logging level to INFO.")
        logging.basicConfig(level=logging.INFO)

    logger.info("Initializing resources...")

    # Initialize environment variables.
    env_file_path = find_dotenv(raise_error_if_not_found=True, usecwd=False)
    logger.info(f"Loading environment variables from {env_file_path}")
    load_dotenv(env_file_path)

    # Enable logging of model checkpoints.
    os.environ["COMET_LOG_ASSETS"] = "True"
    # Set to OFFLINE to run an Offline Experiment or DISABLE to turn off logging
    os.environ["COMET_MODE"] = "ONLINE"
    # Find out more about Comet ML configuration here: https://www.comet.com/docs/v2/integrations/ml-frameworks/huggingface/#configure-comet-for-hugging-face


# TODO: Find a better way to initialize the logger and env vars before importing the rest of the packages.
from training import api, constants, metrics, models

__all__ = ["api", "constants", "metrics", "models"]