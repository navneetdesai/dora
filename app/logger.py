import logging

import colorlog


class Logger(logging.Logger):
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    def __init__(self, name, level=0):
        super().__init__(name, level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-10s%(reset)s[%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors=self.log_colors,
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)
