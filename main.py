"""
Main module for the Synthetic Errands Scheduler

This module serves as the entry point for the application, handling both CLI and GUI modes.
It uses the new configuration management system and implements proper logging and error handling.

Usage:
    python main.py          # Run in GUI mode
    python main.py --cli    # Run in CLI mode
"""

import sys
import logging
from typing import NoReturn

from utils.config_manager import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger: logging.Logger = logging.getLogger(__name__)

def run_cli_mode() -> NoReturn:
    """
    Run the application in CLI mode.
    """
    from cli_interface import cli_main
    cli_main()
    sys.exit(0)

def run_gui_mode() -> NoReturn:
    """
    Run the application in GUI mode.
    """
    try:
        from gui.main_frame import main as gui_main
        logger.info("Starting Synthetic Errands Scheduler in GUI mode")
        gui_main()
        sys.exit(0)
    except ImportError:
        logger.warning("wxPython is not installed. Running in CLI mode instead.")
        logger.info("To run in GUI mode, please install wxPython: pip install -U wxPython")
        run_cli_mode()

def main() -> NoReturn:
    """
    Main function to determine the mode and run the application accordingly.
    """
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--cli":
            run_cli_mode()
        else:
            run_gui_mode()
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Critical error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()