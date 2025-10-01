#!/usr/bin/env python3
"""Demo script to test the logging system without external dependencies."""
import logging
import os
from datetime import datetime
from pathlib import Path


def setup_demo_logging():
    """Set up logging for demo (without python-dotenv dependency)."""
    # Get or create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    # Default log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Always add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
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
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"✓ File logging enabled. Logs will be saved to: {log_file}")
    else:
        logger.info("Console logging only (set SAVE_LOGS=true to enable file logging)")
    
    return logger


def main():
    """Main demo function."""
    print("=" * 70)
    print("LOGGING SYSTEM DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Show current environment variable
    save_logs = os.getenv('SAVE_LOGS', 'false')
    print(f"Current SAVE_LOGS environment variable: {save_logs}")
    print()
    
    # Set up logging
    logger = setup_demo_logging()
    
    print()
    print("Generating sample log messages...")
    print("-" * 70)
    
    # Generate various log levels
    logger.debug("This is a debug message (won't show at INFO level)")
    logger.info("Application started successfully")
    logger.info("Processing data...")
    logger.warning("This is a warning message")
    logger.error("This is an error message (but not critical)")
    logger.info("Operation completed")
    
    print("-" * 70)
    print()
    
    # Show results
    if save_logs.lower() == 'true':
        logs_dir = Path('logs')
        if logs_dir.exists():
            log_files = sorted(logs_dir.glob('*.log'))
            print(f"✓ Log files created in logs/ directory:")
            for log_file in log_files[-5:]:  # Show last 5 files
                size = log_file.stat().st_size
                print(f"  - {log_file.name} ({size} bytes)")
        print()
        print("To view the log file content:")
        print(f"  cat logs/*.log | tail -20")
    else:
        print("File logging is disabled.")
        print()
        print("To enable file logging, run:")
        print("  export SAVE_LOGS=true")
        print("  python3 test_logging_demo.py")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

