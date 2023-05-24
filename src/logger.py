import logging
import sys
import os
from rich.console import Console


# logger for writing to file (extension is .log)
logger = logging.Logger(__name__, "DEBUG")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(f"{os.getcwd()}/crypto.log")
file_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))

logger.addHandler(file_handler)


# logging data to console
console = Console(highlight=False)


def log_twice(lvl: str, msg: str) -> None:
    """Log both from logger and console. Console is for a comfort view, log is to store"""
    match lvl.upper():  # Python >= 3.10
        case "INFO":
            console.print(f"[green] {msg}")
            logger.info(msg)
        case "DEBUG":
            console.print(f"[green] {msg}")
            logger.info(msg)
        case "ERROR":
            console.print(f"[red] {msg}")
            logger.error(msg)
        case "WARN":
            console.print(f"[yellow] {msg}")
            logger.warn(msg)
        case "CRITICAL":
            console.print(f"[red]!!!!!!!!!!!!!{msg}!!!!!!!!!!!!!!!!!")
            logger.critical("!!!!!!!!!!!!!{msg}!!!!!!!!!!!!!!!!!")
            sys.exit()
        case _:
            print(lvl.upper())
            raise AssertionError("There is no such a log level")
