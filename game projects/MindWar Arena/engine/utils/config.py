# engine/utils/config.py

import json
from pathlib import Path

from engine.utils.logger import Logger


class Config:

    _data = {}

    @classmethod
    def load(cls):

        config_path = Path(
            "config/settings.json"
        )

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:

            cls._data = json.load(
                file
            )

        Logger.info(
            "[Config] Loaded"
        )

    @classmethod
    def get(
        cls,
        section,
        key,
        default=None
    ):

        return cls._data.get(
            section,
            {}
        ).get(
            key,
            default
        )