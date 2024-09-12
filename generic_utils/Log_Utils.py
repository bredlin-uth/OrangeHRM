import datetime
import logging
import os

from generic_utils import Config_Utils


def setup_logging(log_dir='test_output/logs'):
    # Create a timestamp
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'orangehrm_{timestamp}.log'
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)
    # Full path to the log file
    log_path = os.path.join(log_dir, log_filename)

    # Full path to the log file
    log_path = os.path.join(log_dir, log_filename)
    # Remove existing handlers to avoid duplicate logs
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler
    file_handler = logging.FileHandler(log_path, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def get_logger(name):
    return logging.getLogger(name)
