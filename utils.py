import subprocess
import logging
from config import LOG_LEVEL


def setup_logger(name, log_file):
    """
    Configures and returns a logger.
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def execute_command(command, logger):
    """
    Executes a shell command and logs its output.
    """
    logger.info(f"Executing command: {command}")
    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        if process.returncode == 0:
            logger.info(f"Command executed successfully: {process.stdout.strip()}")
            return {"status": "success", "output": process.stdout.strip(), "error": None}
        else:
            logger.error(f"Command failed: {process.stderr.strip()}")
            return {"status": "error", "output": None, "error": process.stderr.strip()}
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return {"status": "exception", "output": None, "error": str(e)}

