import logging
import sys

def setup_logging(verbose: bool = False):
    """
    Sets up the logging configuration.
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create logger
    logger = logging.getLogger("notion_sync")
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

def get_logger():
    """Returns the logger instance."""
    return logging.getLogger("notion_sync")
