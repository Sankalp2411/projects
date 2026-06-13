# engine/utils/logger.py

from pathlib import Path
from datetime import datetime


class Logger:

    _log_file = None

    @classmethod
    def initialize(cls):

        log_dir = Path("logs")

        log_dir.mkdir(
            exist_ok=True
        )

        cls._log_file = log_dir / "engine.log"

        with open(
            cls._log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n"
                + "=" * 60
                + "\n"
            )

        cls.info("Logger Initialized")

    @classmethod
    def _write(
        cls,
        level,
        message
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_line = (
            f"{timestamp} "
            f"[{level}] "
            f"{message}"
        )

        print(log_line)

        with open(
            cls._log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                log_line + "\n"
            )

    @classmethod
    def info(
        cls,
        message
    ):

        cls._write(
            "INFO",
            message
        )

    @classmethod
    def warning(
        cls,
        message
    ):

        cls._write(
            "WARNING",
            message
        )

    @classmethod
    def error(
        cls,
        message
    ):

        cls._write(
            "ERROR",
            message
        )

    @classmethod
    def critical(
        cls,
        message
    ):

        cls._write(
            "CRITICAL",
            message
        )

    @classmethod
    def debug(
        cls,
        message
    ):

        cls._write(
            "DEBUG",
            message
        )