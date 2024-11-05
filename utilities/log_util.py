import os
from loguru import logger
from .messagebox import *

def log_error(text):
    logger.error(text)
    MsgBoxError("Error", text + "\n\n\nPlease contact your friendly Test Eng Department")

def configure_logger(filename):
    # Configure logging to log to a file with a specific format
    # Add a new logger with time and size-based rotation
    script_name = os.path.splitext(os.path.basename(filename))[0]

    # Define the directory where logs will be stored
    log_dir = os.path.join(os.path.dirname(os.path.abspath(filename)), "log")

    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a log filename based on the script name and place it in the log directory
    log_filename = os.path.join(log_dir, f"{script_name}.log")

    try:
        logger.add(
            log_filename,
            rotation="5 MB",
            retention="90 days",
            compression="zip",
            level="DEBUG",
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

        # Redirect stderr to the logger
        # CANNOT USE THIS WITH PYTHONW (STDERR DOESN'T EXIST)
        # logger.add(sys.stderr, level="ERROR", backtrace=True, diagnose=True)

        # Ensure no double logging by checking and removing the default stderr handler
        # logger.remove(0)

        logger.info("*************************************************")
        logger.info("*****Logger initialized and logging started.*****")
        logger.info("*************************************************")

        # Flush log
        logger.complete()

    except Exception as e:
        with open("fallback_log.txt", "w") as f:
            f.write(f"Failed to initialize logging: {e}")
        MsgBoxError("Logger Error", f"Failed to initialize logging: {e}")