import logging
import os

# Get the absolute path for the log file
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'invoice_generator.log')

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Create a console handler to also output logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))
logging.getLogger().addHandler(console_handler)

# Log application start
logging.info("Invoice generator application started.")


def log_event(message):
    logging.info(message)


def log_error(error):
    logging.error(error)
