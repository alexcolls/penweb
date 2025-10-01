"""Centralized logging configuration for the application."""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(
    name: Optional[str] = None,
    level: int = logging.INFO,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging with optional file output based on SAVE_LOGS environment variable.
    
    Args:
        name: Logger name (default: root logger)
        level: Logging level (default: INFO)
        log_format: Custom log format string (optional)
        
    Returns:
        Configured logger instance
        
    Environment Variables:
        SAVE_LOGS: Set to 'true' to enable file logging in logs/ directory
    """
    # Get or create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Default log format
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(log_format)
    
    # Always add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Check if file logging is enabled
    save_logs = os.getenv('SAVE_LOGS', 'false').lower() == 'true'
    
    if save_logs:
        # Create logs directory if it doesn't exist
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = logs_dir / f'{timestamp}.log'
        
        # Add file handler
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"File logging enabled. Logs will be saved to: {log_file}")
    else:
        logger.debug("File logging disabled. Set SAVE_LOGS=true to enable.")
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance. If not already configured, it will be set up.
    
    Args:
        name: Logger name (default: root logger)
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # If logger has no handlers, set it up
    if not logger.handlers:
        return setup_logging(name)
    
    return logger

