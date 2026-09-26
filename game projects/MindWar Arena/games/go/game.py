#games/go/game.py
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult
from games.go.ai import GoAI
from games.go.board import GoBoard
from games.go.board_renderer import GoBoardRenderer
from games.go.constants import (ACTION_PASS,FIRST_PLAYER,GAME_DRAW,GAME_MODE_AI_VS_AI,GAME_MODE_HUMAN_VS_AI,GAME_MODE_HUMAN_VS_HUMAN,GAME_NOT_STARTED,GAME_OVER,GAME_RUNNING,PLAYER_BLACK,PLAYER_WHITE,)
from games.go.human_player import HumanPlayer
from games.go.overlay_renderer import GoOverlayRenderer
from games.go.rules import GoRules
class GoGame(GameInterface):
    def __init__(self,renderer,game_mode=GAME_MODE_HUMAN_VS_HUMAN,):
        self.renderer = renderer
        self.game_mode = game_mode
        self.board = GoBoard()
        self.board_renderer = GoBoardRenderer(renderer)
        self.overlay_renderer = GoOverlayRenderer(renderer)
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.consecutive_passes = 0
        self.last_move = None
        self.ko_position = None
        self.previous_board = None
        self.black_controller = None
        self.white_controller = None
        self._create_controllers()
    def initialize(self):
        self.reset()
    def reset(self):
        self.board.reset()
        self.current_player = (self.choose_starting_player())
        self.result.reset()
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.consecutive_passes = 0
        self.last_move = None
        self.ko_position = None
        self.previous_board = None
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        self._reset_controllers()
    def shutdown(self):
        pass
    def _create_controllers(self):
        if self.game_mode == (GAME_MODE_HUMAN_VS_HUMAN):
            self.black_controller = HumanPlayer(self.board_renderer)
            self.white_controller = HumanPlayer(self.board_renderer)
        elif self.game_mode == (GAME_MODE_HUMAN_VS_AI):
            self.black_controller = HumanPlayer(self.board_renderer)
            self.white_controller = GoAI(PLAYER_WHITE)
        elif self.game_mode == (GAME_MODE_AI_VS_AI):
            self.black_controller = GoAI(PLAYER_BLACK)
            self.white_controller = GoAI(PLAYER_WHITE)
        else:
            raise ValueError(f"Invalid Go game mode: "f"{self.game_mode}")
    def _reset_controllers(self):
        if self.black_controller is not None:
            if hasattr(self.black_controller,"reset",):
                self.black_controller.reset()
            if hasattr(self.black_controller,"initialize",):
                self.black_controller.initialize()
            if hasattr(self.black_controller,"set_player",):
                self.black_controller.set_player(PLAYER_BLACK)
        if self.white_controller is not None:
            if hasattr(self.white_controller,"reset",):
                self.white_controller.reset()
            if hasattr(self.white_controller,"initialize",):
                self.white_controller.initialize()
            if hasattr(self.white_controller,"set_player",):
                self.white_controller.set_player(PLAYER_WHITE)
    def update(self):
        if self.is_frozen():
            return
        self.update_current_player()
    def render(self):
        if self.board_renderer is None:
            return
        self.board_renderer.render(board=self.board,legal_moves=self.get_legal_moves(),last_move=self.last_move,ko_position=self.ko_position,)
        self.overlay_renderer.render(result=self.result,board=self.board,consecutive_passes=(self.consecutive_passes),)
    def make_move(self, row, column):
        if self.is_frozen():
            return False
        if not self.board.is_valid_position(row,column,):
            return False
        if not GoRules.is_valid_move(self.board,row,column,self.current_player,self.ko_position,):
            return False
        old_board = self.board.copy()
        if not GoRules.apply_move(self.board,row,column,self.current_player,self.ko_position,):
            return False
        self.previous_board = old_board
        self.move_count += 1
        self.consecutive_passes = 0
        self.last_move = (row, column)
        self._update_ko_position()
        self._switch_player()
        return True
    def pass_turn(self):
        if self.is_frozen():
            return False
        self.previous_board = self.board.copy()
        self.last_move = None
        self.ko_position = None
        self.consecutive_passes += 1
        self.move_count += 1
        if self.consecutive_passes >= 2:
            self._finish_game()
            return True
        self._switch_player()
        return True
    def _finish_game(self):
        self.result = GoRules.evaluate_game(self.board)
        scores = GoRules.get_scores(self.board)
        self.result.scores = scores
        if self.result.draw:
            self.game_state = GAME_DRAW
        else:
            self.game_state = GAME_OVER
    def _update_ko_position(self):
        self.ko_position = None
        if self.previous_board is None:
            return
        current_state = (self.board.get_board_state())
        previous_state = (self.previous_board.get_board_state())
        differences = []
        for row in range(len(current_state)):
            for column in range(len(current_state[row])):
                if (current_state[row][column] != previous_state[row][column]):
                    differences.append((row, column))
        if len(differences) != 1:
            return
        row, column = differences[0]
        if (current_state[row][column] == self.current_player):
            self.ko_position = (row,column,)
    def _switch_player(self):
        if self.current_player == PLAYER_BLACK:
            self.current_player = PLAYER_WHITE
        else:
            self.current_player = PLAYER_BLACK
    def choose_starting_player(self):
        player = self.next_starting_player
        if player == PLAYER_BLACK:
            self.next_starting_player = PLAYER_WHITE
        else:
            self.next_starting_player = PLAYER_BLACK
        return player
    def get_current_controller(self):
        if self.current_player == PLAYER_BLACK:
            return self.black_controller
        if self.current_player == PLAYER_WHITE:
            return self.white_controller
        return None
    def update_current_player(self):
        controller = (self.get_current_controller())
        if controller is None:
            return
        action = controller.get_action(self)
        if action is None:
            return
        if action == ACTION_PASS:
            self.pass_turn()
            return
        if not isinstance(action, tuple):
            return
        if len(action) != 2:
            return
        row, column = action
        self.make_move(row,column,)
    def get_state(self):
        previous_board_state = None
        if self.previous_board is not None:
            previous_board_state = (self.previous_board.get_board_state())
        scores = GoRules.get_scores(self.board)
        return {"board": (self.board.get_board_state()),"previous_board": (previous_board_state),"current_player": (self.current_player),"winner": self.result.winner,"game_state": self.game_state,"game_over": (self.result.game_over),"draw": self.result.draw,"move_count": self.move_count,"consecutive_passes": (self.consecutive_passes),"last_move": self.last_move,"ko_position": self.ko_position,"black_count": (self.board.count_stones(PLAYER_BLACK)),"white_count": (self.board.count_stones(PLAYER_WHITE)),"black_score": scores[PLAYER_BLACK],"white_score": scores[PLAYER_WHITE],"legal_moves": (self.get_legal_moves()),}
    def get_board(self):
        return self.board
    def get_current_player(self):
        return self.current_player
    def get_winner(self):
        return self.result.winner
    def get_result(self):
        return self.result
    def get_game_state(self):
        return self.game_state
    def get_legal_moves(self):
        return GoRules.get_legal_moves(self.board,self.current_player,self.ko_position,)
    def get_black_count(self):
        return self.board.count_stones(PLAYER_BLACK)
    def get_white_count(self):
        return self.board.count_stones(PLAYER_WHITE)
    def get_black_score(self):
        return GoRules.calculate_score(self.board,PLAYER_BLACK,)
    def get_white_score(self):
        return GoRules.calculate_score(self.board,PLAYER_WHITE,)
    def get_last_move(self):
        return self.last_move
    def get_ko_position(self):
        return self.ko_position
    def get_move_count(self):
        return self.move_count
    def get_consecutive_passes(self):
        return self.consecutive_passes
    def is_game_over(self):
        return self.result.game_over
    def is_frozen(self):
        return self.result.game_over
    def is_draw(self):
        return self.result.draw