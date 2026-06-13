# engine/core/input.py

import pygame
from engine.utils.logger import Logger

class Input:
    """
    Centralized input manager.
    """

    _current_keys = None
    _previous_keys = None

    _current_mouse_buttons = (False, False, False)
    _previous_mouse_buttons = (False, False, False)

    _mouse_position = (0, 0)

    @classmethod
    def initialize(cls):

        cls._current_keys = pygame.key.get_pressed()
        cls._previous_keys = pygame.key.get_pressed()

        cls._current_mouse_buttons = pygame.mouse.get_pressed()
        cls._previous_mouse_buttons = pygame.mouse.get_pressed()

        cls._mouse_position = pygame.mouse.get_pos()

        Logger.info("[Input] Initialized")

    @classmethod
    def update(cls):

        cls._previous_keys = cls._current_keys
        cls._current_keys = pygame.key.get_pressed()

        cls._previous_mouse_buttons = cls._current_mouse_buttons
        cls._current_mouse_buttons = pygame.mouse.get_pressed()

        cls._mouse_position = pygame.mouse.get_pos()

    @classmethod
    def is_key_pressed(cls, key):

        return (
            cls._current_keys[key]
            and
            not cls._previous_keys[key]
        )

    @classmethod
    def is_key_held(cls, key):

        return cls._current_keys[key]

    @classmethod
    def is_key_released(cls, key):

        return (
            not cls._current_keys[key]
            and
            cls._previous_keys[key]
        )

    @classmethod
    def is_mouse_pressed(cls, button):

        index = button - 1

        return (
            cls._current_mouse_buttons[index]
            and
            not cls._previous_mouse_buttons[index]
        )

    @classmethod
    def is_mouse_held(cls, button):

        index = button - 1

        return cls._current_mouse_buttons[index]

    @classmethod
    def is_mouse_released(cls, button):

        index = button - 1

        return (
            not cls._current_mouse_buttons[index]
            and
            cls._previous_mouse_buttons[index]
        )

    @classmethod
    def get_mouse_position(cls):

        return cls._mouse_position