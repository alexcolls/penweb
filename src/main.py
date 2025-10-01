"""Main entry point for penweb utilities."""
import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from cli.menu import start_cli


def main():
    """Main function to start the CLI application."""
    start_cli()


if __name__ == "__main__":
    main()

