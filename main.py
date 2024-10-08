"""
Main module for the Synthetic Errands Scheduler
Serves as the entry point for the application in GUI mode.
"""

import sys
import logging
from typing import NoReturn

def setup_logging():
    """Set up logging for the application with reduced noise from third-party loggers."""
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

def run_gui_mode() -> NoReturn:
    """Run the application in GUI mode."""
    try:
        from gui.main_frame import main as gui_main
        
        logger.info("Starting Synthetic Errands Scheduler in GUI mode")
        gui_main()
        sys.exit(0)
    except ImportError as e:
        logger.error(f"ImportError occurred: {str(e)}")
        logger.error("wxPython is not installed or there was an error importing GUI components.")
        logger.info("To run the application, please ensure wxPython is installed: pip install -U wxPython")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error occurred while starting GUI mode: {str(e)}")
        sys.exit(1)

def main() -> NoReturn:
    """Main function to run the application in GUI mode."""
    setup_logging()
    try:
        run_gui_mode()
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Critical error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()