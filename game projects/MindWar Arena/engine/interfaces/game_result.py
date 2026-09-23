# engine/interfaces/game_result.py
from __future__ import annotations
from enum import Enum, auto
from typing import Any
class TerminationReason(Enum):
    NONE = auto()
    CHECKMATE = auto()
    STALEMATE = auto()
    RESIGNATION = auto()
    TIMEOUT = auto()
    DRAW_BY_AGREEMENT = auto()
    DRAW_BY_REPETITION = auto()
    DRAW_BY_50_MOVE = auto()
    DRAW_BY_INSUFFICIENT_MATERIAL = auto()
    NO_LEGAL_MOVES = auto()
    ALL_PIECES_CAPTURED = auto()
    CONSECUTIVE_PASSES = auto()
    WIN_BY_CAPTURES = auto()
    FIVE_IN_A_ROW = auto()
    TERRITORY_SCORING = auto()
class GameResult:
    __slots__ = ("winner","game_over","draw","winning_cells","termination","scores","last_move","move_count",)
    def __init__(self) -> None:
        self.winner: int | None = None
        self.game_over: bool = False
        self.draw: bool = False
        self.winning_cells: list[tuple[int, ...]] = []
        self.termination: TerminationReason = TerminationReason.NONE
        self.scores: dict[int, float] = {}
        self.last_move: Any | None = None
        self.move_count: int = 0
    def reset(self) -> None:
        self.winner = None
        self.game_over = False
        self.draw = False
        self.winning_cells.clear()
        self.termination = TerminationReason.NONE
        self.scores.clear()
        self.last_move = None
        self.move_count = 0
    def has_winner(self) -> bool:
        return self.winner is not None
    def is_draw(self) -> bool:
        return self.draw
    def is_game_over(self) -> bool:
        return self.game_over
    def to_dict(self) -> dict[str, Any]:
        return {"winner": self.winner,"game_over": self.game_over,"draw": self.draw,"winning_cells": list(self.winning_cells),"termination": self.termination.name,"scores": dict(self.scores),"last_move": self.last_move,"move_count": self.move_count,}
    def __repr__(self) -> str:
        parts = [f"GameResult(over={self.game_over}"]
        if self.winner is not None:
            parts.append(f"winner={self.winner}")
        if self.draw:
            parts.append("draw=True")
        if self.termination != TerminationReason.NONE:
            parts.append(f"reason={self.termination.name}")
        return ", ".join(parts) + ")"