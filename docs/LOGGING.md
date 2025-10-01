# Logging System Guide

This project includes a centralized logging system with optional file output controlled by environment variables.

## Quick Start

### 1. Install Dependencies

```bash
poetry install
```

This will install `python-dotenv` which is required for the logging system.

### 2. Create Environment File

Create a `.env` file in the project root:

```bash
# Enable file logging
SAVE_LOGS=true
```

Or copy from the sample:

```bash
cp .env.sample .env
# Edit .env and set SAVE_LOGS=true
```

### 3. Use in Your Code

```python
from dotenv import load_dotenv
from utils.logger import setup_logging

# Load environment variables
load_dotenv()

# Set up logging
logger = setup_logging(__name__)

# Use the logger
logger.info("Application started")
logger.warning("This is a warning")
logger.error("This is an error")
```

## Features

✓ **Automatic Log Directory Creation** - Creates `logs/` folder if it doesn't exist  
✓ **Timestamped Log Files** - Format: `YYYY-MM-DD_HH-MM-SS.log`  
✓ **Console + File Output** - Logs appear in both console and file  
✓ **Environment Control** - Enable/disable with `SAVE_LOGS` variable  
✓ **UTF-8 Encoding** - Supports special characters  
✓ **Configurable Levels** - DEBUG, INFO, WARNING, ERROR, CRITICAL  

## Environment Variables

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `SAVE_LOGS` | `true` / `false` | `false` | Enable file logging |

## Examples

### Example 1: Basic Script

```python
# my_script.py
from dotenv import load_dotenv
from utils.logger import setup_logging

load_dotenv()
logger = setup_logging(__name__)

def main():
    logger.info("Script started")
    try:
        # Your code here
        result = do_something()
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        logger.info("Script finished")

if __name__ == "__main__":
    main()
```

Run with file logging:
```bash
# Set in .env file
echo "SAVE_LOGS=true" > .env
poetry run python my_script.py
```

Or run with environment variable:
```bash
SAVE_LOGS=true poetry run python my_script.py
```

### Example 2: Module with Logging

```python
# utils/my_module.py
from utils.logger import get_logger

logger = get_logger(__name__)

def process_data(data):
    logger.info(f"Processing {len(data)} items")
    
    for item in data:
        try:
            logger.debug(f"Processing item: {item}")
            # Process item
        except Exception as e:
            logger.error(f"Failed to process {item}: {e}")
    
    logger.info("Processing complete")
```

### Example 3: Custom Log Level

```python
from dotenv import load_dotenv
from utils.logger import setup_logging
import logging

load_dotenv()

# Set custom log level
logger = setup_logging(__name__, level=logging.DEBUG)

logger.debug("This debug message will now appear")
logger.info("Info message")
logger.warning("Warning message")
```

## Log Output Format

Default format:
```
YYYY-MM-DD HH:MM:SS,mmm - module_name - LEVEL - message
```

Example:
```
2025-10-01 14:32:25,479 - __main__ - INFO - Application started successfully
2025-10-01 14:32:25,480 - __main__ - WARNING - This is a warning message
2025-10-01 14:32:25,481 - __main__ - ERROR - This is an error message
```

## File Structure

When `SAVE_LOGS=true`:

```
blue-yellow/
├── logs/                           # Created automatically
│   ├── 2025-10-01_14-32-25.log    # First run
│   ├── 2025-10-01_15-45-10.log    # Second run
│   └── 2025-10-02_09-20-33.log    # Another run
├── .env                            # Your environment config
├── .env.sample                     # Template file
└── src/
    ├── main.py                     # Example usage
    └── utils/
        ├── logger.py               # Logging utility
        └── README_LOGGING.md       # Detailed docs
```

## Integration with Existing Code

### Lambda Function

The Lambda function can use the logging system for local testing:

```python
# src/lambda/entrypoint_with_logging.py
from utils.logger import setup_logging

logger = setup_logging(__name__)

def lambda_handler(event, context):
    logger.info("Lambda invoked")
    # ... rest of code
```

For AWS deployment, the logger will automatically fall back to standard logging if `python-dotenv` is not available.

### Utility Scripts

Update your utility modules:

```python
# Before
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# After
from utils.logger import get_logger
logger = get_logger(__name__)
```

## Running Without File Logging

If you don't create a `.env` file or set `SAVE_LOGS=false`, logging will only output to console:

```bash
# Console only
poetry run python src/main.py

# With file logging
SAVE_LOGS=true poetry run python src/main.py
```

## Log Management

### View Recent Logs

```bash
# View all logs
cat logs/*.log

# View last 20 lines
tail -20 logs/*.log

# View specific log file
cat logs/2025-10-01_14-32-25.log

# Follow logs in real-time (if running)
tail -f logs/2025-10-01_14-32-25.log
```

### Clean Up Old Logs

```bash
# Remove logs older than 7 days
find logs/ -name "*.log" -mtime +7 -delete

# Remove all logs
rm -rf logs/
```

### Log Rotation (Optional)

For production use, consider implementing log rotation:

```python
from logging.handlers import RotatingFileHandler

# Max 10MB per file, keep 5 backup files
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,
    backupCount=5
)
```

## Troubleshooting

### Issue: Logs not being saved to file

**Solution:**
1. Check `.env` file exists: `cat .env`
2. Verify `SAVE_LOGS=true` (no spaces around `=`)
3. Ensure `python-dotenv` is installed: `poetry install`
4. Check you're calling `load_dotenv()` before `setup_logging()`

### Issue: Permission denied when creating logs/

**Solution:**
```bash
# Check permissions
ls -ld .

# Make directory writable
chmod u+w .
```

### Issue: Import error for utils.logger

**Solution:**
Make sure you're running from the project root:
```bash
cd /path/to/blue-yellow
poetry run python src/main.py
```

### Issue: Duplicate log messages

**Solution:**
Don't call `setup_logging()` multiple times. Use `get_logger()` instead:

```python
# In main.py - call once
logger = setup_logging(__name__)

# In other modules - use get_logger
from utils.logger import get_logger
logger = get_logger(__name__)
```

## Advanced Configuration

### Custom Log Format

```python
from utils.logger import setup_logging

logger = setup_logging(
    name=__name__,
    log_format='[%(levelname)s] %(asctime)s - %(message)s'
)
```

### Multiple Loggers

```python
# Different loggers for different modules
api_logger = setup_logging('api', level=logging.DEBUG)
db_logger = setup_logging('database', level=logging.WARNING)

api_logger.debug("API call received")
db_logger.warning("Slow query detected")
```

### Conditional Logging

```python
import os
from utils.logger import setup_logging, get_logger
import logging

# More verbose logging in development
level = logging.DEBUG if os.getenv('ENV') == 'dev' else logging.INFO
logger = setup_logging(__name__, level=level)
```

## Best Practices

1. **Always load environment first**: Call `load_dotenv()` at the top of your main file
2. **One setup per application**: Call `setup_logging()` once in your main entry point
3. **Use get_logger in modules**: Other modules should use `get_logger(__name__)`
4. **Log meaningful messages**: Include context, not just "Error occurred"
5. **Use appropriate levels**: DEBUG for details, INFO for progress, WARNING for issues, ERROR for failures
6. **Don't log sensitive data**: Avoid logging passwords, tokens, or personal information
7. **Clean up old logs**: Implement a log rotation or cleanup strategy

## See Also

- [README_LOGGING.md](src/utils/README_LOGGING.md) - Detailed documentation
- [.env.sample](.env.sample) - Environment variable template
- [logger.py](src/utils/logger.py) - Logger implementation

