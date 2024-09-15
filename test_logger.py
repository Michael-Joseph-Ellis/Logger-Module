import logger

logger.setup_logging()

# testing logger 
def main():
    # you can do , extra = {"x": "hello"} inside of this logging statement to capture extras
    logger.a_logger.debug("debug")
    logger.a_logger.info("info")
    logger.a_logger.warning("warning")
    logger.a_logger.error("error")
    logger.a_logger.critical("critical")
    logger.a_logger.exception("exception")
    
    try: 
        # Intentional syntax error
        test(something)
    except Exception as e:
        # Log the exception
        logger.a_logger.exception(f"Exception: {e}")

main()

# NOTE: 
# The log file is stored in the 'logs' directory relative to the script's location.
# The log file is named 'Logs.log.jsonl' and contains logs in JSON format.
# The log file is created if it doesn't exist.
# The log file is appended to if it already exists.
# The log file contains all log records, including debug and info logs.
# The log file does not contain error logs (warning, error, critical, and exception logs). But these can be added by removing the NonErrorFilter filter.
# The log file contains the log records in JSON Lines format.
# The log file contains the log records in the following format:
#     {
#         "timestamp": "2021-07-17 14:31:19,123",
#         "level": "INFO",
#         "name": "my_logger",
#         "message": "Logging setup complete."
#     }
#     {
#         "timestamp": "2021-07-17 14:31:19,123",
#         "level": "DEBUG",
#         "name": "my_logger",
#         "message": "debug"
#     }
# This is just a small example of how to use the logger. You can customize the logger further by adding more handlers, filters, and formatters as needed. 
# You can also configure the logger to log to different destinations such as files, console, email, and more.
# The logger can be used to log messages, exceptions, and other information in a structured and configurable way.