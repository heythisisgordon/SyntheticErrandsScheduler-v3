"""
Main module for the Synthetic Errands Scheduler
Serves as the entry point for the application in GUI mode.
"""

import sys
import logging
from typing import NoReturn
from profile_visualization import run_with_profile

def _setup_logging():
    """Set up logging for the application"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("wx").setLevel(logging.WARNING)

logger: logging.Logger = logging.getLogger(__name__)

def _run_gui_mode() -> NoReturn:
    """Run the application in GUI mode."""
    try:
        from controllers.application_controller import ApplicationController
        
        logger.info("Starting ApplicationController...")
        app_controller = ApplicationController()
        app_controller.run()
        
        logger.info("ApplicationController finished running.")
    except ImportError as e:
        logger.error(f"GUI components import error: {str(e)}")
        logger.error("Please ensure wxPython is installed: pip install -U wxPython")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error in GUI mode: {str(e)}")
        sys.exit(1)

def _main() -> NoReturn:
    """Main function to run the application in GUI mode."""
    _setup_logging()
    logger.info("Starting main function...")
    try:
        run_with_profile(_run_gui_mode)
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")
    except Exception as e:
        logger.exception(f"Critical error: {str(e)}")
    finally:
        logger.info("Program finished.")
        sys.exit(0)

if __name__ == "__main__":
    _main()
