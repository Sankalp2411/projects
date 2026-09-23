# engine/board/grid_board.py
from __future__ import annotations
import random
from typing import Any
from engine.interfaces.board_interface import BoardInterface
class GridBoard(BoardInterface):
    def __init__(self,rows: int = 8,columns: int = 8,empty_value: int = 0,*,num_piece_types: int = 16,) -> None:
        self.rows: int = rows
        self.columns: int = columns
        self.empty_value: int = empty_value
        self._board: list[list[int]] = []
        self._move_stack: list[dict[str, Any]] = []
        self._redo_stack: list[dict[str, Any]] = []
        self._zobrist_table: list[list[list[int]]] = []
        self._zobrist_hash: int = 0
        self._num_piece_types: int = num_piece_types
        self._init_zobrist()
        self.reset()
    def _init_zobrist(self) -> None:
        rng = random.Random(42)
        self._zobrist_table = [[[rng.getrandbits(64) for _ in range(self._num_piece_types)] for _ in range(self.columns)] for _ in range(self.rows)]
    def _compute_zobrist(self) -> int:
        h = 0
        for r in range(self.rows):
            for c in range(self.columns):
                piece = self._board[r][c]
                if piece != self.empty_value and piece < self._num_piece_types:
                    h ^= self._zobrist_table[r][c][piece]
        return h
    def _update_zobrist(self, row: int, col: int, old_val: int, new_val: int) -> None:
        if old_val != self.empty_value and old_val < self._num_piece_types:
            self._zobrist_hash ^= self._zobrist_table[row][col][old_val]
        if new_val != self.empty_value and new_val < self._num_piece_types:
            self._zobrist_hash ^= self._zobrist_table[row][col][new_val]
    def reset(self) -> None:
        self._board = [[self.empty_value for _ in range(self.columns)] for _ in range(self.rows)]
        self._move_stack.clear()
        self._redo_stack.clear()
        self._zobrist_hash = 0
    def copy(self) -> GridBoard:
        new_board = GridBoard(self.rows,self.columns,self.empty_value,num_piece_types=self._num_piece_types,)
        new_board._board = [row[:] for row in self._board]
        new_board._zobrist_hash = self._zobrist_hash
        new_board._zobrist_table = self._zobrist_table
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
    def place_piece(self, row: int, col: int, value: int) -> bool:
        return self.set_cell(row, col, value)
    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.columns
    def is_cell_empty(self, row: int, col: int) -> bool:
        if not self.is_valid_position(row, col):
            return False
        return self._board[row][col] == self.empty_value
    def is_empty(self, row: int, col: int) -> bool:
        return self.is_cell_empty(row, col)
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
        return (self.rows, self.columns)
    def get_available_moves(self) -> list[tuple[int, int]]:
        moves: list[tuple[int, int]] = []
        for r in range(self.rows):
            for c in range(self.columns):
                if self._board[r][c] == self.empty_value:
                    moves.append((r, c))
        return moves
    def make_move(self,row: int,col: int,value: int,*,extra: dict[str, Any] | None = None,) -> bool:
        if not self.is_valid_position(row, col):
            return False
        old_value = self._board[row][col]
        record: dict[str, Any] = {"row": row,"col": col,"old_value": old_value,"new_value": value,}
        if extra is not None:
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
        self._redo_stack.append(record)
        return True
    def redo_move(self) -> bool:
        if not self._redo_stack:
            return False
        record = self._redo_stack.pop()
        self.set_cell(record["row"], record["col"], record["new_value"])
        self._move_stack.append(record)
        return True
    def can_undo(self) -> bool:
        return bool(self._move_stack)
    def can_redo(self) -> bool:
        return bool(self._redo_stack)
    def count_pieces(self, value: int) -> int:
        count = 0
        for row in self._board:
            for cell in row:
                if cell == value:
                    count += 1
        return count
    def find_pieces(self, value: int) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for r in range(self.rows):
            for c in range(self.columns):
                if self._board[r][c] == value:
                    positions.append((r, c))
        return positions
    def find_first(self, value: int) -> tuple[int, int] | None:
        for r in range(self.rows):
            for c in range(self.columns):
                if self._board[r][c] == value:
                    return (r, c)
        return None
    def __str__(self) -> str:
        lines: list[str] = []
        for row in self._board:
            lines.append(" ".join(str(c) for c in row))
        return "\n".join(lines)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GridBoard):
            return NotImplemented
        return self._board == other._board
    def __hash__(self) -> int:
        return self._zobrist_hash