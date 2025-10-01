"""Configuration management for penweb application."""
import os
from pathlib import Path
from typing import Optional

# Try to load dotenv
try:
    from dotenv import load_dotenv
    # Load .env from project root
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # dotenv not installed, will use system environment variables


def get_output_dir() -> Path:
    """
    Get the configured output directory from environment variables.
    
    Returns:
        Path: The output directory path (default: .output)
    """
    output_dir = os.getenv("OUTPUT_DIR", ".output")
    
    # Make it absolute if it's relative
    path = Path(output_dir)
    if not path.is_absolute():
        # Resolve relative to project root
        project_root = Path(__file__).parent.parent.parent
        path = project_root / output_dir
    
    return path


def get_clone_output_dir(subdirectory: Optional[str] = None) -> Path:
    """
    Get the output directory for cloned websites.
    
    Args:
        subdirectory: Optional subdirectory name within the output dir
        
    Returns:
        Path: The clone output directory path
    """
    output_dir = get_output_dir()
    
    if subdirectory:
        return output_dir / subdirectory
    else:
        return output_dir / "cloned_site"


def ensure_output_dir_exists() -> None:
    """Ensure the output directory exists."""
    output_dir = get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)


# For backward compatibility and easy imports
OUTPUT_DIR = get_output_dir()
