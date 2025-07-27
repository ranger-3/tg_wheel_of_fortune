import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Final

from rich.logging import RichHandler

LOG_LEVEL: Final = logging.INFO
LOG_FILE: Final = "bot.log"
LOG_DIR: Final = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("bot")
logger.setLevel(LOG_LEVEL)
logger.propagate = False

console_handler = RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)
console_handler.setLevel(LOG_LEVEL)

file_handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    when="midnight",
    interval=1,
    backupCount=0,
    encoding="utf-8",
)
file_handler.setLevel(LOG_LEVEL)

console_formatter = logging.Formatter("%(message)s")
file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
