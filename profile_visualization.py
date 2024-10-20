import cProfile
import pstats
import io
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_with_profile(func):
    """Run the given function with profiling and save the results."""
    logger.info("Starting profiling...")
    profiler = cProfile.Profile()
    profiler.enable()
    
    func()
    
    profiler.disable()
    
    logger.info("Profiling completed. Saving results...")
    
    # Print the stats to a string
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    ps.print_stats()
    
    # Write the stats to a file
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'application_profile.txt')
    with open(file_path, 'w') as f:
        f.write(s.getvalue())
    
    logger.info(f"Profile saved as {file_path}")

if __name__ == "__main__":
    logger.info("profile_visualization.py executed directly")
    run_with_profile(lambda: print("Test run"))
