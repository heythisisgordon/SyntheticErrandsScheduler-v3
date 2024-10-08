"""
Main module for the Synthetic Errands Scheduler

This module serves as the entry point for the application, handling both CLI and GUI modes.
It uses the new configuration management system and implements proper logging and error handling.

Usage:
    python main.py                      # Run in GUI mode
    python main.py --cli                # Run in CLI mode with default optimizer (CP-SAT)
    python main.py --cli --optimizer vrp  # Run in CLI mode with VRP optimizer
"""

import sys
import logging
import argparse
from typing import NoReturn
from utils.config_manager import config

def setup_logging():
    """Set up logging for the application."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Set third-party loggers to a higher level to reduce noise
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("wx").setLevel(logging.WARNING)

logger: logging.Logger = logging.getLogger(__name__)

def run_cli_mode(optimizer: str) -> NoReturn:
    """
    Run the application in CLI mode.

    Args:
        optimizer (str): The chosen optimizer ('cp-sat' or 'vrp')
    """
    from cli_interface import cli_main
    cli_main(optimizer)
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
    except ImportError as e:
        logger.error(f"ImportError occurred: {str(e)}")
        logger.warning("wxPython is not installed or there was an error importing GUI components. Running in CLI mode instead.")
        logger.info("To run in GUI mode, please ensure wxPython is installed: pip install -U wxPython")
        run_cli_mode("cp-sat")  # Default to CP-SAT optimizer if running in CLI mode due to missing wxPython
    except Exception as e:
        logger.exception(f"Unexpected error occurred while starting GUI mode: {str(e)}")
        sys.exit(1)

def main() -> NoReturn:
    """
    Main function to determine the mode and run the application accordingly.
    """
    setup_logging()
    logger.info("Starting Synthetic Errands Scheduler")

    parser = argparse.ArgumentParser(description="Synthetic Errands Scheduler")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--optimizer", choices=["cp-sat", "vrp"], default="cp-sat",
                        help="Choose the optimization algorithm for CLI mode (default: cp-sat)")
    args = parser.parse_args()

    try:
        if args.cli:
            logger.info(f"Running in CLI mode with {args.optimizer} optimizer")
            run_cli_mode(args.optimizer)
        else:
            run_gui_mode()
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Critical error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()