import logging
import yaml


logger = logging.getLogger(__name__)


def read_yaml_file(file_path):
    """
    Load a YAML file and return its contents as a Python dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: A dictionary containing the YAML configuration.
    """
    try:
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config
    except FileNotFoundError:
        logger.error("Config file not found at %s", file_path)
        return {}
    except yaml.YAMLError as e:
        logger.error("Failed to load YAML from %s. %s", file_path, e)
        return {}



