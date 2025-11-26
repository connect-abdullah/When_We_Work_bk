import logging


def get_logger(name, level=logging.DEBUG):
    """Get a configured logger instance.
    
    Args:
        name (str): Name of the logger, typically __name__ of the module
        level (int): Log level to use. Available levels are:
            - logging.DEBUG (10): Detailed information for debugging
            - logging.INFO (20): General information about program execution
            - logging.WARNING (30): Indicate a potential problem
            - logging.ERROR (40): More serious problem
            - logging.CRITICAL (50): Program may not be able to continue
            
    Example:
        logger = get_logger(__name__, level=logging.INFO)
        logger.debug("Debug message") # Won't show if level=INFO
        logger.info("Info message")  # Will show
        logger.error("Error message") # Will show
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Check if handlers already exist
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(levelname)s: %(asctime)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.propagate = (
            False  # Prevent the logger from propagating to the root logger
        )
    return logger
