"""
MindWar Arena

input.py

Centralized input management.

Responsibilities
----------------
• Keyboard input
• Mouse position
• Mouse button states
• Mouse click detection

This module is engine-level and reusable by every game.
"""

import pygame

from engine.utils.logger import Logger


class Input:

    # ---------------------------------------------------------
    # Keyboard
    # ---------------------------------------------------------

    _pressed_keys = set()
    _previous_keys = set()
    _key_clicked = set()
    # ---------------------------------------------------------
    # Mouse
    # ---------------------------------------------------------

    _mouse_x = 0
    _mouse_y = 0

    _left_pressed = False
    _previous_left_pressed = False
    _left_clicked = False

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    @classmethod
    def initialize(cls):

        cls._pressed_keys = set()

        cls._keys_down = set()

        cls._keys_up = set()    

        cls._mouse_x = 0
        cls._mouse_y = 0

        cls._left_pressed = False
        cls._previous_left_pressed = False
        cls._left_clicked = False

        Logger.info("[Input] Initialized")

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    @classmethod
    def update(cls, events):

        # --------------------------------------------
        # Reset one-frame states
        # --------------------------------------------

        cls._keys_down.clear()

        cls._keys_up.clear()

        cls._left_clicked = False

        # --------------------------------------------
        # Mouse position
        # --------------------------------------------

        cls._mouse_x, cls._mouse_y = pygame.mouse.get_pos()

        # --------------------------------------------
        # Process events
        # --------------------------------------------

        for event in events:

            if event.type == pygame.KEYDOWN:

                cls._pressed_keys.add(event.key)

                cls._keys_down.add(event.key)

            elif event.type == pygame.KEYUP:

                cls._pressed_keys.discard(event.key)

                cls._keys_up.add(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    cls._left_pressed = True

                    cls._left_clicked = True

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:

                    cls._left_pressed = False
    # ---------------------------------------------------------
    # Keyboard API
    # ---------------------------------------------------------

    @classmethod
    def is_key_pressed(cls, key):

        return key in cls._pressed_keys

    # ---------------------------------------------------------
    # Mouse API
    # ---------------------------------------------------------

    @classmethod
    def is_key_clicked(cls, key):

        return key in cls._keys_down

    @classmethod
    def get_mouse_position(cls):

        return (
            cls._mouse_x,
            cls._mouse_y,
        )

    @classmethod
    def get_mouse_x(cls):

        return cls._mouse_x

    @classmethod
    def get_mouse_y(cls):

        return cls._mouse_y

    @classmethod
    def is_left_mouse_pressed(cls):

        return cls._left_pressed

    @classmethod
    def is_left_mouse_clicked(cls):

        return cls._left_clicked
    
    @classmethod
    def is_key_released(cls, key):

        return key in cls._keys_up