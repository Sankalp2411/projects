#games/nine_mens_morris/game.py
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import GameResult
from games.nine_mens_morris.ai import NineMensMorrisAI
from games.nine_mens_morris.board import NineMensMorrisBoard
from games.nine_mens_morris.board_renderer import BoardRenderer
from games.nine_mens_morris.constants import (PLAYER_BLACK,PLAYER_WHITE,FIRST_PLAYER,GAME_NOT_STARTED,GAME_RUNNING,GAME_DRAW,GAME_OVER,GAME_MODE_HUMAN_VS_HUMAN,GAME_MODE_HUMAN_VS_AI,PHASE_PLACEMENT,PHASE_MOVEMENT,PHASE_FLYING,PIECES_PER_PLAYER,)
from games.nine_mens_morris.human_player import HumanPlayer
from games.nine_mens_morris.overlay_renderer import OverlayRenderer
from games.nine_mens_morris.rules import NineMensMorrisRules
class NineMensMorrisGame(GameInterface):
    def __init__(self,renderer,game_mode=GAME_MODE_HUMAN_VS_HUMAN,):
        self.renderer = renderer
        self.game_mode = game_mode
        self.board = NineMensMorrisBoard()
        self.current_player = FIRST_PLAYER
        self.next_starting_player = FIRST_PLAYER
        self.result = GameResult()
        self.game_state = GAME_NOT_STARTED
        self.move_count = 0
        self.pieces_placed = {PLAYER_BLACK: 0,PLAYER_WHITE: 0,}
        self.capture_pending = False
        self.board_renderer = BoardRenderer(renderer)
        self.overlay_renderer = OverlayRenderer(renderer)
        self.human_player = HumanPlayer(self.board_renderer)
        self.ai_player = NineMensMorrisAI()
        self.player_black = self.human_player
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.player_white = self.ai_player
        else:
            self.player_white = self.human_player
    def initialize(self):
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.ai_player.initialize()
        self.reset()
    def reset(self):
        self.board.reset()
        self.choose_starting_player()
        self.result = GameResult()
        self.pieces_placed = {PLAYER_BLACK: 0,PLAYER_WHITE: 0,}
        self.capture_pending = False
        self.game_state = GAME_RUNNING
        self.move_count = 0
        self.board_renderer.reset()
        self.overlay_renderer.reset()
        self.human_player.reset()
        if self.game_mode == GAME_MODE_HUMAN_VS_AI:
            self.ai_player.reset()
            self.ai_player.initialize()
    def shutdown(self):
        pass
    def update(self):
        if self.is_frozen():
            return
        if self.capture_pending:
            self.update_capture_controller()
            return
        self.update_current_player()
    def render(self):
        selected_position = (self.human_player.selected_position)
        self.board_renderer.render(self.board,self.result,selected_position,)
        self.overlay_renderer.render(self.result)
        self.render_information()
    def render_information(self):
        phase_name = self.get_phase_name()
        self.renderer.draw_text(f"Phase: {phase_name}",(700, 80),size=28,)
        self.renderer.draw_text(f"Black: {self.board.count_pieces(PLAYER_BLACK)}",(700, 125),size=26,)
        self.renderer.draw_text(f"White: {self.board.count_pieces(PLAYER_WHITE)}",(700, 165),size=26,)
        if self.capture_pending:
            self.renderer.draw_text("Select an opponent piece to remove",(700, 225),size=24,)
        else:
            current_name = ("Black"if self.current_player == PLAYER_BLACK else "White")
            self.renderer.draw_text(f"Turn: {current_name}",(700, 225),size=26,)
    def make_move(self, *args):
        if self.is_frozen():
            return False
        if self.capture_pending:
            if len(args) != 1:
                return False
            return self.remove_opponent_piece(args[0])
        phase = self.get_phase()
        if phase == PHASE_PLACEMENT:
            if len(args) != 1:
                return False
            return self.place_piece(args[0])
        if phase in (PHASE_MOVEMENT,PHASE_FLYING,):
            if len(args) != 2:
                return False
            return self.move_piece(args[0],args[1],)
        return False
    def place_piece(self, position):
        if not self.board.is_valid_position(position):
            return False
        if not self.board.is_position_empty(position):
            return False
        if (self.pieces_placed[self.current_player] >= PIECES_PER_PLAYER):
            return False
        if not self.board.place_piece(position,self.current_player,):
            return False
        self.pieces_placed[self.current_player] += 1
        self.move_count += 1
        if NineMensMorrisRules.is_mill(self.board,position,self.current_player,):
            self.capture_pending = True
            removable = (NineMensMorrisRules.get_removable_pieces(self.board,self.current_player,))
            if not removable:
                self.capture_pending = False
                self.switch_player()
            return True
        self.switch_player()
        return True
    def move_piece(self, source, destination):
        if not self.board.is_valid_position(source):
            return False
        if not self.board.is_valid_position(destination):
            return False
        if self.board.get_position(source) != self.current_player:
            return False
        if not self.board.is_position_empty(destination):
            return False
        legal_destinations = (
            NineMensMorrisRules.get_legal_destinations(self.board,source,self.current_player,))
        if destination not in legal_destinations:
            return False
        if not self.board.move_piece(source,destination,self.current_player,):
            return False
        self.move_count += 1
        if NineMensMorrisRules.is_mill(self.board,destination,self.current_player,):
            self.capture_pending = True
            removable = (NineMensMorrisRules.get_removable_pieces(self.board,self.current_player,))
            if not removable:
                self.capture_pending = False
                self.check_game_result()
                if not self.is_frozen():
                    self.switch_player()
            return True
        self.check_game_result()
        if self.is_frozen():
            return True
        self.switch_player()
        return True
    def remove_opponent_piece(self, position):
        if not self.capture_pending:
            return False
        if not NineMensMorrisRules.can_remove_piece(self.board,position,self.current_player,):
            return False
        if not self.board.remove_piece(position):
            return False
        self.capture_pending = False
        self.check_game_result()
        if self.is_frozen():
            return True
        self.switch_player()
        return True
    def check_game_result(self):
        if self.get_phase() == PHASE_PLACEMENT:
            return
        opponent = (NineMensMorrisRules.get_opponent(self.current_player))
        if opponent == 0:
            return
        if self.board.count_pieces(opponent) < 3:
            self.result = GameResult()
            self.result.winner = (self.current_player)
            self.result.game_over = True
            self.game_state = GAME_OVER
            return
        if not NineMensMorrisRules.has_legal_move(self.board,opponent,):
            self.result = GameResult()
            self.result.winner = (self.current_player)
            self.result.game_over = True
            self.game_state = GAME_OVER
            return
        if self.board.is_board_full():
            self.result = GameResult()
            self.result.draw = True
            self.result.game_over = True
            self.game_state = GAME_DRAW
    def switch_player(self):
        if self.current_player == PLAYER_BLACK:
            self.current_player = PLAYER_WHITE
        else:
            self.current_player = PLAYER_BLACK
    def choose_starting_player(self):
        self.current_player = (self.next_starting_player)
        if self.next_starting_player == PLAYER_BLACK:
            self.next_starting_player = PLAYER_WHITE
        else:
            self.next_starting_player = PLAYER_BLACK
    def get_current_controller(self):
        if self.current_player == PLAYER_BLACK:
            return self.player_black
        return self.player_white
    def update_current_player(self):
        controller = (self.get_current_controller())
        move = controller.get_action(self)
        if move is None:
            return
        if isinstance(move, tuple):
            self.make_move(*move)
        else:
            self.make_move(move)
    def update_capture_controller(self):
        controller = (self.get_current_controller())
        move = controller.get_action(self)
        if move is None:
            return
        if isinstance(move, tuple):
            return
        self.make_move(move)
    def get_result(self):
        return self.result
    def get_board(self):
        return self.board
    def get_current_player(self):
        return self.current_player
    def get_phase(self):
        if (self.pieces_placed[PLAYER_BLACK] < PIECES_PER_PLAYER or self.pieces_placed[PLAYER_WHITE] < PIECES_PER_PLAYER):
            return PHASE_PLACEMENT
        if NineMensMorrisRules.can_fly(self.board,self.current_player,):
            return PHASE_FLYING
        return PHASE_MOVEMENT
    def get_phase_name(self):
        phase = self.get_phase()
        if phase == PHASE_PLACEMENT:
            return "Placement"
        if phase == PHASE_MOVEMENT:
            return "Movement"
        if phase == PHASE_FLYING:
            return "Flying"
        return "Unknown"
    def is_capture_pending(self):
        return self.capture_pending
    def get_piece_count(self, player):
        return self.board.count_pieces(player)
    def get_piece_counts(self):
        return {PLAYER_BLACK: self.board.count_pieces(PLAYER_BLACK),PLAYER_WHITE: self.board.count_pieces(PLAYER_WHITE),}
    def get_state(self):
        return {"board": self.board.get_board_state(),"current_player": self.current_player,"winner": self.result.winner,"game_state": self.game_state,"game_over": self.result.game_over,"draw": self.result.draw,"move_count": self.move_count,"phase": self.get_phase(),"pieces_placed": dict(self.pieces_placed),"capture_pending": self.capture_pending,"flying": (NineMensMorrisRules.can_fly(self.board,self.current_player,)),}
    def is_game_over(self):
        return self.is_frozen()
    def get_winner(self):
        return self.result.winner
    def is_frozen(self):
        return self.result.game_over