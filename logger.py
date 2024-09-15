import logging.config
import json
import logging.handlers
from pathlib import Path
import datetime as dt
from typing_extensions import override

# Set of built-in logging attributes
LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName"
}

class MyJSONFormatter(logging.Formatter):
    """
    A custom logging formatter that formats log records as JSON objects.

    Args:
        fmt_keys (dict[str, str], optional): A dictionary that maps log record keys to their desired
            output key names in the JSON format. Defaults to None.

    Preconditions:
        - `fmt_keys` must be a dictionary mapping log record attributes to their corresponding keys in the output.

    Postconditions:
        - Log messages will be formatted as JSON strings containing the specified attributes.

    Methods:
        format(record): Formats the log record as a JSON string.
        _prepare_log_dict(record): Prepares the log record dictionary before conversion to JSON.

    Returns:
        str: A formatted JSON string representing the log message.

    Example:
        >>> logger = logging.getLogger("my_logger")
        >>> formatter = MyJSONFormatter(fmt_keys={"message": "msg", "timestamp": "time"})
        >>> logger.setFormatter(formatter)
    """
    
    def __init__(self, *, fmt_keys: dict[str, str] | None = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        """
        Prepares the log record as a dictionary for JSON serialization.

        Args:
            record (logging.LogRecord): The log record object.

        Returns:
            dict: A dictionary containing the log record's attributes and values.

        Example:
            >>> record = logging.makeLogRecord({"msg": "Test log"})
            >>> formatter = MyJSONFormatter()
            >>> formatted_log = formatter._prepare_log_dict(record)
        """
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }

        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatException(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message

class NonErrorFilter(logging.Filter):
    """
    A logging filter that allows only non-error logs (INFO level and below).

    Methods:
        filter(record): Filters log records based on their log level.

    Args:
        record (logging.LogRecord): The log record to filter.

    Returns:
        bool: True if the record's log level is less than or equal to INFO, otherwise False.

    Example:
        >>> logger = logging.getLogger("my_logger")
        >>> filter = NonErrorFilter()
        >>> logger.addFilter(filter)
    """

    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO

def setup_logging():
    """
    Sets up the logging configuration using a JSON configuration file and 
    dynamically adjusts the log file location.

    Preconditions:
        - A valid logging configuration file (logging_config.json) must be present in 
          the 'logging_configs' directory relative to the script's location.
        - A 'logs' directory will be created if it doesn't exist.

    Postconditions:
        - Logging is configured as per the JSON configuration.
        - The log file is set to be stored in the 'logs' directory.

    Vars:
        log_dir (Path): The path to the log directory.
        log_file (Path): The path to the JSON log file.
        config_file (Path): The path to the logging configuration file.

    Returns:
        None: The function configures the logger and does not return any value.

    Example:
        >>> setup_logging()
        >>> logger = logging.getLogger("my_logger")
        >>> logger.info("Logging setup complete.")
    """
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # set up log file location relative to the script location and create the log file
    log_file = log_dir / "Logs.log.jsonl"

    # load logging config from JSON file in the 'logging_configs' directory
    config_file = Path(__file__).parent / "logging_configs/logging_config.json"
    with open(config_file) as f_in:
        config = json.load(f_in)

    # update the filename in the configuration to use the dynamically determined path to the log file
    if 'handlers' in config and 'file_json' in config['handlers']: 
        config['handlers']['file_json']['filename'] = str(log_file)

    # configure logging using the updated configuration
    logging.config.dictConfig(config)

# Initialize logger for use in the rest of the program (can change the name as needed to fit the program context)
a_logger = logging.getLogger("my_logger")