"""
Handles logging for the application.
"""
import logging

import colorlog


class Logger(logging.Logger):
    """
    Custom logger class that uses colorlog to colorize the output.
    """

    log_colors = {  # setup colors for each log level
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    def __init__(self, name, level=0):
        """
        Initialize the logger.
        :param name: name of the logger
        :param level: logging level
        """
        super().__init__(name, level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = colorlog.ColoredFormatter(  # set up the formatter
            "%(log_color)s%(levelname)-10s%(reset)s[%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=self.log_colors,
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)
