# engine/board/intersection_board.py
from __future__ import annotations
import random
from typing import Any
from engine.interfaces.board_interface import BoardInterface
class IntersectionBoard(BoardInterface):
    def __init__(self,size: int = 19,empty_value: int = 0,*,num_piece_types: int = 4,) -> None:
        self.size: int = size
        self.rows: int = size
        self.columns: int = size
        self.empty_value: int = empty_value
        self._board: list[list[int]] = []
        self._move_stack: list[dict[str, Any]] = []
        self._redo_stack: list[dict[str, Any]] = []
        self._num_piece_types: int = num_piece_types
        self._zobrist_table: list[list[list[int]]] = []
        self._zobrist_hash: int = 0
        self._init_zobrist()
        self._position_history: list[int] = []
        self.reset()
    def _init_zobrist(self) -> None:
        rng = random.Random(123)
        self._zobrist_table = [[[rng.getrandbits(64) for _ in range(self._num_piece_types)] for _ in range(self.size)] for _ in range(self.size)]
    def _update_zobrist(self, row: int, col: int, old_val: int, new_val: int) -> None:
        if old_val != self.empty_value and old_val < self._num_piece_types:
            self._zobrist_hash ^= self._zobrist_table[row][col][old_val]
        if new_val != self.empty_value and new_val < self._num_piece_types:
            self._zobrist_hash ^= self._zobrist_table[row][col][new_val]
    def reset(self) -> None:
        self._board = [[self.empty_value for _ in range(self.size)] for _ in range(self.size)]
        self._move_stack.clear()
        self._redo_stack.clear()
        self._zobrist_hash = 0
        self._position_history.clear()
    def copy(self) -> IntersectionBoard:
        new_board = IntersectionBoard(self.size,self.empty_value,num_piece_types=self._num_piece_types,)
        new_board._board = [row[:] for row in self._board]
        new_board._zobrist_hash = self._zobrist_hash
        new_board._zobrist_table = self._zobrist_table
        new_board._position_history = list(self._position_history)
        return new_board
    def get_cell(self, row: int, col: int) -> int:
        return self._board[row][col]
    def set_cell(self, row: int, col: int, value: int) -> bool:
        if not self.is_valid_position(row, col):
            return False
        old = self._board[row][col]
        self._board[row][col] = value
        self._update_zobrist(row, col, old, value)
        return True
    def get_intersection(self, row: int, col: int) -> int:
        return self.get_cell(row, col)
    def set_intersection(self, row: int, col: int, value: int) -> bool:
        return self.set_cell(row, col, value)
    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size
    def is_cell_empty(self, row: int, col: int) -> bool:
        if not self.is_valid_position(row, col):
            return False
        return self._board[row][col] == self.empty_value
    def place_stone(self, row: int, col: int, player: int) -> bool:
        if not self.is_cell_empty(row, col):
            return False
        return self.set_cell(row, col, player)
    def remove_stone(self, row: int, col: int) -> bool:
        if self.is_cell_empty(row, col):
            return False
        return self.set_cell(row, col, self.empty_value)
    def count_stones(self, player: int) -> int:
        count = 0
        for row in self._board:
            for cell in row:
                if cell == player:
                    count += 1
        return count
    def get_player_positions(self, player: int) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for r in range(self.size):
            for c in range(self.size):
                if self._board[r][c] == player:
                    positions.append((r, c))
        return positions
    def push_position(self) -> None:
        self._position_history.append(self._zobrist_hash)
    def is_superko_violation(self) -> bool:
        return self._zobrist_hash in self._position_history
    def get_board_state(self) -> list[list[int]]:
        return [row[:] for row in self._board]
    def get_board_hash(self) -> int:
        return self._zobrist_hash
    def is_board_full(self) -> bool:
        for row in self._board:
            for cell in row:
                if cell == self.empty_value:
                    return False
        return True
    def get_dimensions(self) -> tuple[int, int]:
        return (self.size, self.size)
    def get_available_moves(self) -> list[tuple[int, int]]:
        moves: list[tuple[int, int]] = []
        for r in range(self.size):
            for c in range(self.size):
                if self._board[r][c] == self.empty_value:
                    moves.append((r, c))
        return moves
    def make_move(self,row: int,col: int,value: int,*,captured: list[tuple[int, int, int]] | None = None,extra: dict[str, Any] | None = None,) -> bool:
        if not self.is_valid_position(row, col):
            return False
        record: dict[str, Any] = {"row": row,"col": col,"old_value": self._board[row][col],"new_value": value,"captured": captured or [],}
        if extra:
            record["extra"] = extra
        self.set_cell(row, col, value)
        self._move_stack.append(record)
        self._redo_stack.clear()
        return True
    def undo_move(self) -> bool:
        if not self._move_stack:
            return False
        record = self._move_stack.pop()
        self.set_cell(record["row"], record["col"], record["old_value"])
        for r, c, old_val in record.get("captured", []):
            self.set_cell(r, c, old_val)
        if self._position_history:
            self._position_history.pop()
        self._redo_stack.append(record)
        return True
    def redo_move(self) -> bool:
        if not self._redo_stack:
            return False
        record = self._redo_stack.pop()
        for r, c, _ in record.get("captured", []):
            self.set_cell(r, c, self.empty_value)
        self.set_cell(record["row"], record["col"], record["new_value"])
        self.push_position()
        self._move_stack.append(record)
        return True
    def can_undo(self) -> bool:
        return bool(self._move_stack)
    def can_redo(self) -> bool:
        return bool(self._redo_stack)
    def __str__(self) -> str:
        symbols = {self.empty_value: ".", 1: "●", 2: "○"}
        lines: list[str] = []
        for row in self._board:
            lines.append(" ".join(symbols.get(c, str(c)) for c in row))
        return "\n".join(lines)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntersectionBoard):
            return NotImplemented
        return self._board == other._board
    def __hash__(self) -> int:
        return self._zobrist_hash