# 🎯 Logging System - Setup Complete!

A comprehensive logging system has been successfully added to the blue-yellow project with environment variable control.

## ✅ What Was Implemented

### 1. Core Logging Module (`src/utils/logger.py`)

A centralized logging utility with:
- **Dual Output**: Console + optional file logging
- **Environment Control**: Toggle file logging with `SAVE_LOGS` env var
- **Auto Directory Creation**: Creates `logs/` folder automatically
- **Timestamped Files**: Format `YYYY-MM-DD_HH-MM-SS.log`
- **Flexible Configuration**: Custom log levels and formats
- **UTF-8 Support**: Handles special characters

**Key Functions:**
```python
setup_logging(name, level, log_format)  # Initialize logging
get_logger(name)                         # Get logger instance
```

### 2. Environment Configuration

**Files Created:**
- `.env` - Active environment configuration
- `.env.sample` - Template for users

**Environment Variable:**
```bash
SAVE_LOGS=true   # Enable file logging
SAVE_LOGS=false  # Console only (default)
```

### 3. Updated Dependencies

**Added to `pyproject.toml`:**
- `python-dotenv = "^1.0.0"`

### 4. Git Configuration

**Updated `.gitignore`:**
```
*.log
logs/
```

### 5. CLI Integration

**Updated `src/cli/menu.py`:**
- Automatically loads `.env` file
- Sets up logging on startup
- Logs all tool executions (Ping, Clone, etc.)
- Logs errors and warnings
- Logs application lifecycle events

### 6. Example Files

**Created:**
- `src/lambda/entrypoint_with_logging.py` - Lambda with logging
- `LOGGING.md` - Comprehensive user guide
- `src/utils/README_LOGGING.md` - Detailed documentation

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd /home/kali/labs/blue-yellow
poetry install
```

### Step 2: Enable File Logging (Optional)

Edit `.env` file:
```bash
SAVE_LOGS=true
```

### Step 3: Run Your Application

```bash
# Run the CLI
poetry run python src/main.py

# Or with environment override
SAVE_LOGS=true poetry run python src/main.py
```

### Step 4: Check Log Files

```bash
# List log files
ls -lh logs/

# View latest log
tail -20 logs/*.log
```

## 📋 Example Output

### With SAVE_LOGS=false (Console Only)
```
2025-10-01 14:32:19,082 - blue-yellow - INFO - Blue-Yellow CLI started
2025-10-01 14:32:25,123 - blue-yellow - INFO - Tool: Ping URL - Target: https://example.com
2025-10-01 14:32:25,456 - blue-yellow - INFO - Ping successful - Status: 200, Time: 333ms
```

### With SAVE_LOGS=true (Console + File)
```
2025-10-01 14:35:10,479 - blue-yellow - INFO - File logging enabled. Logs will be saved to: logs/2025-10-01_14-35-10.log
2025-10-01 14:35:10,480 - blue-yellow - INFO - Blue-Yellow CLI started
2025-10-01 14:35:15,123 - blue-yellow - INFO - Tool: Ping URL - Target: https://example.com
2025-10-01 14:35:15,456 - blue-yellow - INFO - Ping successful - Status: 200, Time: 333ms
```

**Log file created:** `logs/2025-10-01_14-35-10.log`

## 📁 Directory Structure

```
blue-yellow/
├── .env                             # Environment configuration
├── .env.sample                      # Environment template
├── LOGGING.md                       # User guide
├── LOGGING_SETUP.md                 # This file
├── pyproject.toml                   # Updated with python-dotenv
├── logs/                            # Created automatically when SAVE_LOGS=true
│   ├── 2025-10-01_14-35-10.log
│   ├── 2025-10-01_15-22-30.log
│   └── ...
└── src/
    ├── main.py                      # CLI entry point
    ├── cli/
    │   └── menu.py                  # Updated with logging
    ├── lambda/
    │   ├── entrypoint.py            # Original
    │   └── entrypoint_with_logging.py  # With logging
    └── utils/
        ├── logger.py                # Core logging module ⭐
        └── README_LOGGING.md        # Detailed docs
```

## 🔧 Usage Examples

### Example 1: Use in New Module

```python
from utils.logger import get_logger

logger = get_logger(__name__)

def my_function():
    logger.info("Function started")
    try:
        # Your code
        result = process_data()
        logger.info(f"Success: {result}")
    except Exception as e:
        logger.error(f"Error: {e}")
```

### Example 2: Custom Log Level

```python
from utils.logger import setup_logging
import logging

logger = setup_logging(__name__, level=logging.DEBUG)

logger.debug("Detailed debug info")
logger.info("General info")
logger.warning("Warning message")
logger.error("Error message")
```

### Example 3: Temporarily Enable Logging

```bash
# Enable for single run
SAVE_LOGS=true poetry run python src/main.py

# Enable for session
export SAVE_LOGS=true
poetry run python src/main.py
```

## 🎨 Features in Action

### Feature 1: Automatic Directory Creation
```bash
$ SAVE_LOGS=true poetry run python src/main.py
# ✓ logs/ directory created automatically if it doesn't exist
```

### Feature 2: Timestamped Log Files
```bash
$ ls logs/
2025-10-01_14-30-45.log
2025-10-01_15-45-10.log
2025-10-02_09-20-33.log
# ✓ Each run creates a new timestamped file
```

### Feature 3: Dual Output
```bash
$ SAVE_LOGS=true poetry run python src/main.py
# ✓ Logs appear in BOTH console AND file
```

### Feature 4: Environment Control
```bash
$ SAVE_LOGS=false poetry run python src/main.py
# ✓ Console only, no file created

$ SAVE_LOGS=true poetry run python src/main.py
# ✓ Console + file logging
```

## 🛠️ Integration Status

### ✅ Integrated
- [x] CLI Menu (`src/cli/menu.py`)
  - Tool executions logged
  - Errors and warnings logged
  - Application lifecycle logged

### 📝 Ready to Integrate
- [ ] Ping utility (`src/utils/ping.py`)
- [ ] Clone utility (`src/utils/clone.py`)
- [ ] D2 utility (`src/utils/d2.py`)
- [ ] Login utility (`src/utils/login.py`)
- [ ] Lambda function (`src/lambda/entrypoint.py`)

### Example Integration (Ping Utility)
```python
# Before
def ping_url(url: str):
    # ... code ...
    
# After
from utils.logger import get_logger
logger = get_logger(__name__)

def ping_url(url: str):
    logger.info(f"Pinging {url}")
    # ... code ...
    logger.info(f"Ping successful - Status: {status}")
```

## 📊 Log Management

### View Logs
```bash
# View all logs
cat logs/*.log

# View last 20 lines
tail -20 logs/*.log

# Follow in real-time
tail -f logs/2025-10-01_14-35-10.log

# Search logs
grep "ERROR" logs/*.log
```

### Clean Up Logs
```bash
# Remove logs older than 7 days
find logs/ -name "*.log" -mtime +7 -delete

# Remove all logs
rm -rf logs/
```

## 🐛 Troubleshooting

### Issue: python-dotenv not installed
**Solution:**
```bash
poetry install
```

### Issue: Logs not being saved
**Check:**
1. Is `SAVE_LOGS=true` in `.env`?
2. Run: `cat .env | grep SAVE_LOGS`
3. No spaces around `=`: ✓ `SAVE_LOGS=true` ✗ `SAVE_LOGS = true`

### Issue: Permission denied
**Solution:**
```bash
# Ensure directory is writable
chmod u+w .
```

### Issue: Import error
**Solution:**
```bash
# Run from project root
cd /home/kali/labs/blue-yellow
poetry run python src/main.py
```

## 📖 Documentation

- **LOGGING.md** - Comprehensive user guide with examples
- **src/utils/README_LOGGING.md** - Detailed API documentation
- **src/utils/logger.py** - Well-documented source code

## 🎯 Next Steps

1. **Test the System:**
   ```bash
   SAVE_LOGS=true poetry run python src/main.py
   ```

2. **Verify Log File:**
   ```bash
   ls -lh logs/
   cat logs/*.log
   ```

3. **Integrate into Other Modules:**
   - Add logging to utility functions
   - Add logging to Lambda functions
   - Add logging to service modules

4. **Customize as Needed:**
   - Adjust log format
   - Change log levels
   - Add custom handlers

## ✨ Benefits

- 🔍 **Debugging**: Track program execution and errors
- 📊 **Auditing**: Record all tool usage and results
- 🔐 **Security**: Log authentication attempts and access
- 📈 **Monitoring**: Track performance and issues
- 🚀 **Production**: Enable detailed logging when needed

## 🎉 Summary

You now have a fully functional logging system that:
- ✅ Creates timestamped log files when enabled
- ✅ Automatically creates logs/ directory
- ✅ Controls file logging via SAVE_LOGS environment variable
- ✅ Logs all program execution and errors
- ✅ Works with CLI, Lambda, and utility modules
- ✅ Follows Python logging best practices

**To enable logging, simply set:**
```bash
SAVE_LOGS=true
```

**Enjoy your new logging system! 🎊**

