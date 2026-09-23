# engine/utils/serialization.py
from __future__ import annotations
import json
from typing import Any
STARTING_CHESS_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
CHESS_PIECE_TO_FEN = {1: "P",2: "N",3: "B",4: "R",5: "Q",6: "K",-1: "p",-2: "n",-3: "b",-4: "r",-5: "q",-6: "k",0: "",}
FEN_TO_CHESS_PIECE = {v: k for k, v in CHESS_PIECE_TO_FEN.items() if v}
def board_to_fen(board: list[list[int]],turn: str = "w",castling: str = "KQkq",en_passant: str = "-",halfmove: int = 0,fullmove: int = 1,) -> str:
    rows = []
    for r in range(8):
        empty_count = 0
        row_str = ""
        for c in range(8):
            piece = board[r][c]
            symbol = CHESS_PIECE_TO_FEN.get(piece, "")
            if symbol == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    row_str += str(empty_count)
                    empty_count = 0
                row_str += symbol
        if empty_count > 0:
            row_str += str(empty_count)
        rows.append(row_str)
    placement = "/".join(rows)
    return f"{placement} {turn} {castling} {en_passant} {halfmove} {fullmove}"
def fen_to_board(fen: str) -> tuple[list[list[int]], str, str, str, int, int]:
    parts = fen.strip().split()
    if len(parts) < 1:
        raise ValueError("Invalid FEN string")
    placement = parts[0]
    turn = parts[1] if len(parts) > 1 else "w"
    castling = parts[2] if len(parts) > 2 else "-"
    en_passant = parts[3] if len(parts) > 3 else "-"
    halfmove = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0
    fullmove = int(parts[5]) if len(parts) > 5 and parts[5].isdigit() else 1
    board: list[list[int]] = []
    for row_str in placement.split("/"):
        row: list[int] = []
        for ch in row_str:
            if ch.isdigit():
                row.extend([0] * int(ch))
            else:
                row.append(FEN_TO_CHESS_PIECE.get(ch, 0))
        if len(row) < 8:
            row.extend([0] * (8 - len(row)))
        board.append(row[:8])
    while len(board) < 8:
        board.append([0] * 8)
    return board[:8], turn, castling, en_passant, halfmove, fullmove
def coords_to_sgf(row: int, col: int) -> str:
    return f"{chr(ord('a') + col)}{chr(ord('a') + row)}"
def sgf_to_coords(sgf_coord: str) -> tuple[int, int]:
    if len(sgf_coord) < 2:
        return (0, 0)
    col = ord(sgf_coord[0].lower()) - ord("a")
    row = ord(sgf_coord[1].lower()) - ord("a")
    return (row, col)
def export_sgf(game_name: str,moves: list[tuple[str, tuple[int, int] | str]],board_size: int = 19,result: str = "?",) -> str:
    header = f"(;GM[1]FF[4]CA[UTF-8]AP[MindWarArena]SZ[{board_size}]GN[{game_name}]RE[{result}]\n"
    move_nodes = []
    for player, mv in moves:
        p_tag = "B" if player.upper().startswith("B") or player == "1" else "W"
        if mv == "pass" or mv is None:
            coord_str = ""
        elif isinstance(mv, (tuple, list)) and len(mv) >= 2:
            coord_str = coords_to_sgf(mv[0], mv[1])
        else:
            coord_str = ""
        move_nodes.append(f";{p_tag}[{coord_str}]")
    return header + "".join(move_nodes) + "\n)"
def export_pgn(event: str = "MindWar Arena Match",site: str = "Local Engine",white: str = "Player 1",black: str = "Player 2",result: str = "*",move_list: list[str] | None = None,) -> str:
    headers = [f'[Event "{event}"]',f'[Site "{site}"]',f'[White "{white}"]',f'[Black "{black}"]',f'[Result "{result}"]',]
    body = []
    if move_list:
        for i in range(0, len(move_list), 2):
            move_num = (i // 2) + 1
            w_move = move_list[i]
            b_move = move_list[i + 1] if i + 1 < len(move_list) else ""
            if b_move:
                body.append(f"{move_num}. {w_move} {b_move}")
            else:
                body.append(f"{move_num}. {w_move}")
    body_text = " ".join(body)
    if result and result != "*":
        body_text += f" {result}"
    return "\n".join(headers) + "\n\n" + body_text + "\n"
def export_pdn(event: str = "MindWar Checkers",white: str = "Player 1",black: str = "Player 2",result: str = "*",move_list: list[str] | None = None,) -> str:
    headers = [f'[Event "{event}"]','[GameType "20"]',f'[White "{white}"]',f'[Black "{black}"]',f'[Result "{result}"]',]
    body = " ".join(move_list) if move_list else ""
    return "\n".join(headers) + "\n\n" + body + f" {result}\n"
def serialize_game_state(state: dict[str, Any]) -> str:
    return json.dumps(state, default=lambda o: str(o), indent=2)
def deserialize_game_state(json_str: str) -> dict[str, Any]:
    return json.loads(json_str)