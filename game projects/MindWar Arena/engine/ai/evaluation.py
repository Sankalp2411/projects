# engine/ai/evaluation.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, state: Any) -> float:
        pass
    @staticmethod
    def material_count(board: Any,piece_values: dict[int, float],player: int,opponent: int,) -> float:
        dims = board.get_dimensions()
        rows, cols = dims[0], dims[1] if len(dims) > 1 else dims[0]
        player_score = 0.0
        opponent_score = 0.0
        for r in range(rows):
            for c in range(cols):
                piece = board.get_cell(r, c)
                value = piece_values.get(piece, 0.0)
                if value > 0:
                    player_score += value
        return player_score - opponent_score
    @staticmethod
    def mobility_score(legal_moves_player: int,legal_moves_opponent: int,weight: float = 0.1,) -> float:
        return weight * (legal_moves_player - legal_moves_opponent)
    @staticmethod
    def centre_control_score(board: Any,player: int,rows: int,cols: int,weight: float = 0.3,) -> float:
        centre_r = rows / 2.0
        centre_c = cols / 2.0
        max_dist = max(centre_r, centre_c)
        if max_dist == 0:
            return 0.0
        score = 0.0
        for r in range(rows):
            for c in range(cols):
                if board.get_cell(r, c) == player:
                    dist = abs(r - centre_r) + abs(c - centre_c)
                    score += weight * (1.0 - dist / (2.0 * max_dist))
        return score
    @staticmethod
    def piece_square_value(board: Any,tables: dict[int, list[list[float]]],rows: int,cols: int,) -> float:
        score = 0.0
        for r in range(rows):
            for c in range(cols):
                piece = board.get_cell(r, c)
                table = tables.get(piece)
                if table is not None and r < len(table) and c < len(table[r]):
                    score += table[r][c]
        return score
    @staticmethod
    def connectivity_score(positions: list[tuple[int, int]],weight: float = 0.05,) -> float:
        pos_set = set(positions)
        score = 0.0
        for r, c in positions:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (r + dr, c + dc) in pos_set:
                    score += weight
        return score / 2.0
