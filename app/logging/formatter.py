import logging


class ColoredFormatter(logging.Formatter):
    colors = {
        "DEBUG": "\033[38m",  # grey
        "INFO": "\033[36m",  # cyan
        "WARNING": "\033[33m",  # yellow
        "ERROR": "\033[31m",  # red
        "CRITICAL": "\033[35m",  # magenta
    }
    reset = "\033[0m"

    def format(self, record):
        color = self.colors.get(record.levelname, self.reset)
        message = super().format(record)
        return f"{color}{message}{self.reset}"
