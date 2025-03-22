import logging
from rich.logging import RichHandler

import os
import sys


__parent_dir = os.path.dirname(
    os.path.dirname(
        os.path.abspath(
            __file__
            )
        )
    )

if __parent_dir not in sys.path:
    sys.path.insert(
        0,
        __parent_dir
    )


from downedit.utils.logger import log
from downedit.utils.logger import Formatter, init_logging


def test_singleton():
    logger1 = init_logging()
    logger2 = init_logging()
    logger3 = logging.getLogger("DownEdit")

    print("Logger 1 id:", id(logger1))
    print("Logger 2 id:", id(logger2))
    print("Logger 3 id:", id(logger3))

    assert logger1 is logger2, "Logger instances are not the same"
    assert logger2 is logger3, "Logger instances are not the same"
    assert logger1 is logger3, "Logger instances are not the same"

    print("All logger instances are the same")

# Test logging functionality
def test_logging():
    logger = init_logging()
    print("test_logging id:", id(logger))
    logger.info("hello world")
    logger.debug("debug info")
    logger.error("error info")
    logger.warning("warning info")
    logger.critical("critical info")
    logger.file("File operation performed successfully.")
    logger.pause()

# Test different log levels
def test_log_levels():
    logger = init_logging()
    logger.setLevel(logging.DEBUG)
    print("init_logging id:", id(logger))
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    logger.file("This is a custom file level message")

# Test logger configuration
def test_logger_configuration():
    logger = init_logging()
    assert logger.level == logging.DEBUG, "Logger level is not set correctly"
    assert isinstance(logger.handlers[0], RichHandler), "Handler is not of type RichHandler"
    print("test_logger_configuration id:", id(logger))
    logger.pause()
    
# Test logger with multiple handlers
def test_multiple_handlers():
    logger = init_logging()
    file_handler = logging.FileHandler('test.log')
    file_handler.setFormatter(Formatter())
    logger.addHandler(file_handler)

    logger.info("This is a test message with multiple handlers")
    print("test_multiple_handlers id:", id(logger))
    logger.removeHandler(file_handler)
    file_handler.close()
    os.remove('test.log')

# Main test execution
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    # Run the singleton test
    test_singleton()
    # Run the logging test
    test_logging()
    # Run the log levels test
    test_log_levels()
    # Run the logger configuration test
    test_logger_configuration()
    # Run the multiple handlers test
    test_multiple_handlers()
    print("Before close", log.handlers)
    log.close()
    print("After close", log.handlers)