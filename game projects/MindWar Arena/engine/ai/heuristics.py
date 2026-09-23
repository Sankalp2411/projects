# engine/ai/heuristics.py
from __future__ import annotations
from typing import Any
def count_lines_of_length(board: Any,player: int,length: int,rows: int,cols: int,directions: list[tuple[int, int]],empty_value: int = 0,) -> int:
    count = 0
    visited: set = set()
    for r in range(rows):
        for c in range(cols):
            if board.get_cell(r, c) != player:
                continue
            for dr, dc in directions:
                key = (r, c, dr, dc)
                if key in visited:
                    continue
                consecutive = 0
                cr, cc = r, c
                while 0 <= cr < rows and 0 <= cc < cols and board.get_cell(cr, cc) == player:
                    consecutive += 1
                    cr += dr
                    cc += dc
                if consecutive != length:
                    continue
                br, bc = r - dr, c - dc
                open_before = (0 <= br < rows and 0 <= bc < cols and board.get_cell(br, bc) == empty_value)
                open_after = (0 <= cr < rows and 0 <= cc < cols and board.get_cell(cr, cc) == empty_value)
                if open_before or open_after:
                    count += 1
                    for i in range(consecutive):
                        visited.add((r + i * dr, c + i * dc, dr, dc))
    return count
def line_threat_score(board: Any,player: int,win_length: int,rows: int,cols: int,directions: list[tuple[int, int]],empty_value: int = 0,) -> float:
    score = 0.0
    for length in range(2, win_length + 1):
        count = count_lines_of_length(board, player, length, rows, cols, directions, empty_value)
        weight = 10.0 ** (length - 1)
        score += count * weight
    return score
def capture_advantage(player_pieces: int,opponent_pieces: int,weight: float = 1.0,) -> float:
    return weight * (player_pieces - opponent_pieces)
def territory_score(player_territory: int,opponent_territory: int,weight: float = 1.0,) -> float:
    return weight * (player_territory - opponent_territory)
def king_safety_penalty(king_exposure: int,weight: float = -0.5,) -> float:
    return weight * king_exposure
def pawn_structure_score(doubled_pawns: int,isolated_pawns: int,passed_pawns: int,) -> float:
    return -0.5 * doubled_pawns - 0.5 * isolated_pawns + 1.0 * passed_pawns
def mill_count_score(player_mills: int,opponent_mills: int,weight: float = 5.0,) -> float:
    return weight * (player_mills - opponent_mills)
def potential_mill_score(player_potential: int,opponent_potential: int,weight: float = 2.0,) -> float:
    return weight * (player_potential - opponent_potential)