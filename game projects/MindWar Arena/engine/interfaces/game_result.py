#engine/interfaces/game_result.py
class GameResult:
    def __init__(self):
        self.winner = None
        self.game_over = False
        self.draw = False
        self.winning_cells = []
    def reset(self):
        self.winner = None
        self.game_over = False
        self.draw = False
        self.winning_cells.clear()
    def has_winner(self):
        return self.winner is not None
    def is_draw(self):
        return self.draw
    def is_game_over(self):
        return self.game_over