# /* LogManager.py */ #

# COPYRIGHT (C) 2025 antalervin19
# I do NOT give ANYONE permission to copy, modify or redistribute code in this file!
# If you want to use code from this in your own project(s), you HAVE to ask me for permission first!
# Contacts:
# Discord: antalervin19
# Web: https://www.iggames.eu

import configparser
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path("./Logs")
CONFIG_FILE = Path("./Config.ini")
LOGS_DIR.mkdir(exist_ok=True)

DEFAULT_CONFIG = {
    "Logging": {
        "show_console": "false",
        "log_console": "true"
    }
}
if not CONFIG_FILE.exists():
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

show_console = config.getboolean("Logging", "show_console", fallback=True)
log_console = config.getboolean("Logging", "log_console", fallback=True)

def get_next_log_file():
    index = 0
    while True:
        log_name = f"Console_{index:04}.log"
        log_path = LOGS_DIR / log_name
        if not log_path.exists():
            return log_path
        index += 1

LOG_FILE = get_next_log_file()

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}]: {message}"

    if show_console:
        print(formatted)

    if log_console:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")