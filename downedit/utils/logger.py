import datetime
import logging
import time

from rich.logging import RichHandler
from rich.traceback import install
from rich.console import Console

from .singleton import Singleton

install()

class Formatter(logging.Formatter):
    msg_color = {
        "DEBUG"     : "green",
        "INFO"      : "cyan",
        "WARNING"   : "yellow",
        "ERROR"     : "red",
        "CRITICAL"  : "bold red",
        "FILE"      : "magenta",
    }

    def __init__(self, fmt="{message}", style='{', datefmt="[%X]"):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        """
        Format the message with color based on the log level
        """
        # Retrieve the original message
        message = record.getMessage()
        color = self.msg_color.get(record.levelname, 'white')
        message = f"[{color}]| {message}[/]"
        record.msg = message
        return super().format(record)
    

class Logger(logging.Logger, metaclass=Singleton):
    _console_instance = None
    
    def __init__(self, name, level=logging.DEBUG):
        if hasattr(self, '_ready'):
            return
        
        if Logger._console_instance is None:
            Logger._console_instance = Console()
        
        super().__init__(name, level)
        self.console = Logger._console_instance
        self._ready = True

    def config_log(self, log_level=logging.INFO):
        """
        Set new log level and configure 
        """
        self.setLevel(log_level)
        if not self.hasHandlers():
            console_handler = RichHandler(
                show_time=True,
                show_path=False,
                markup=True,
                rich_tracebacks=True,
                omit_repeated_times=False
            )
            console_handler.setFormatter(Formatter())
            self.addHandler(console_handler)
    
    def pause(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.console.input(f"[cyan][{current_time}][/] [green]Press any key to continue ...[/]")

    def close(self):
        # Properly close and remove all handlers
        for handler in self.handlers:
            handler.close()
            self.removeHandler(handler)
        self.handlers.clear()
        # Ensure all logs are processed before exit
        time.sleep(0.5)
        

# Set the custom logger class as the default
logging.setLoggerClass(Logger)

# Adding custom log level method
FILE_LEVEL_NUM = 25
logging.addLevelName(FILE_LEVEL_NUM, "FILE")

def file(self, message, *args, **kwargs):
    if self.isEnabledFor(FILE_LEVEL_NUM):
        self._log(FILE_LEVEL_NUM, message, args, **kwargs)

logging.Logger.file = file

def init_logging():
    logger = logging.getLogger("DownEdit")
    if not logger.handlers:
        logger.config_log(log_level=logging.DEBUG)
    return logger

# Initialize the logger
logger = init_logging()