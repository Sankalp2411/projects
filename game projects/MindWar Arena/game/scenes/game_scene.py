# game/scenes/game_scene.py
from __future__ import annotations
from pathlib import Path
import pygame
from engine.core.input import Input
from engine.core.scene import Scene
from engine.interfaces.game_interface import GameInterface
from engine.interfaces.game_result import TerminationReason
from engine.utils.constants import DEFAULT_TURN_TIME_LIMIT, GameMode, GameState
from engine.utils.logger import Logger
class GameScene(Scene):
    def __init__(self, game: GameInterface) -> None:
        super().__init__("Game Scene")
        if not isinstance(game, GameInterface):
            raise TypeError("GameScene requires an object implementing GameInterface.")
        self.game = game
        self.hint_message: str | None = None
        self.hint_timer: float = 0.0
        self.ai_move_timer: float = 0.0
        self.ai_move_delay: float = 0.6
        self.turn_timer: float = DEFAULT_TURN_TIME_LIMIT
        self.last_player: int | None = None
    def enter(self) -> None:
        super().enter()
        Logger.info("[GameScene] Initializing game.")
        self.game.initialize()
        self.hint_message = None
        self.hint_timer = 0.0
        self.ai_move_timer = 0.0
        self.turn_timer = DEFAULT_TURN_TIME_LIMIT
        self.last_player = getattr(self.game, "current_player", None)
    def exit(self) -> None:
        Logger.info("[GameScene] Shutting down game.")
        self.game.shutdown()
        super().exit()
    def update(self) -> None:
        dt = self.time_manager.get_delta_time() if self.time_manager else (1.0 / 60.0)
        curr_player = getattr(self.game, "current_player", None)
        if curr_player != self.last_player:
            self.last_player = curr_player
            self.turn_timer = DEFAULT_TURN_TIME_LIMIT
        is_ai_vs_ai = getattr(self.game, "game_mode", None) == GameMode.AI_VS_AI
        if is_ai_vs_ai and not self.game.is_game_over():
            self.ai_move_timer += dt
            if self.ai_move_timer >= self.ai_move_delay:
                self.ai_move_timer = 0.0
                self.game.update()
        else:
            self.game.update()
            if not self.game.is_game_over():
                self.turn_timer -= dt
                if self.turn_timer <= 0.0:
                    self.turn_timer = 0.0
                    result = getattr(self.game, "result", None)
                    if result is not None and not result.game_over:
                        result.game_over = True
                        result.termination = TerminationReason.TIMEOUT
                        if hasattr(self.game, "switch_player"):
                            self.game.switch_player()
                            result.winner = self.game.get_current_player()
                            self.game.switch_player()
                        else:
                            curr = getattr(self.game, "current_player", 1)
                            result.winner = 2 if curr == 1 else 1
                        if hasattr(self.game, "game_state"):
                            self.game.game_state = GameState.OVER
                        Logger.info(f"[GameScene] Turn timeout! Player {curr_player} forfeited.")
        if self.hint_timer > 0.0:
            self.hint_timer -= dt
            if self.hint_timer <= 0.0:
                self.hint_timer = 0.0
                self.hint_message = None
        ctrl_held = Input.is_key_pressed(pygame.K_LCTRL) or Input.is_key_pressed(pygame.K_RCTRL)
        if (ctrl_held and Input.is_key_clicked(pygame.K_z)) or Input.is_key_clicked(pygame.K_u):
            if self.game.can_undo():
                self.game.undo()
                self.turn_timer = DEFAULT_TURN_TIME_LIMIT
                Logger.info("[GameScene] Move undone.")
        elif ctrl_held and Input.is_key_clicked(pygame.K_y):
            if self.game.can_redo():
                self.game.redo()
                self.turn_timer = DEFAULT_TURN_TIME_LIMIT
                Logger.info("[GameScene] Move redone.")
        elif Input.is_key_clicked(pygame.K_h):
            hint = self.game.get_hint()
            if hint is not None:
                self.hint_message = f"Hint: {hint}"
                self.hint_timer = 3.0
                Logger.info(f"[GameScene] Hint requested: {hint}")
            else:
                self.hint_message = "No hint available"
                self.hint_timer = 1.5
        elif Input.is_key_clicked(pygame.K_SPACE) or Input.is_key_clicked(pygame.K_p):
            if hasattr(self.game, "pass_turn"):
                self.game.pass_turn()
                self.turn_timer = DEFAULT_TURN_TIME_LIMIT
                Logger.info("[GameScene] Passed turn.")
        elif Input.is_key_clicked(pygame.K_q):
            if not self.game.is_game_over():
                result = getattr(self.game, "result", None)
                if result is not None:
                    result.game_over = True
                    result.termination = TerminationReason.RESIGNATION
                    if hasattr(self.game, "switch_player"):
                        self.game.switch_player()
                        result.winner = self.game.get_current_player()
                        self.game.switch_player()
                    Logger.info("[GameScene] Player resigned.")
        elif ctrl_held and Input.is_key_clicked(pygame.K_e):
            self._export_game()
        elif Input.is_key_clicked(pygame.K_r):
            self.game.reset()
            self.hint_message = None
            self.ai_move_timer = 0.0
            self.turn_timer = DEFAULT_TURN_TIME_LIMIT
            Logger.info("[GameScene] Game reset.")
        elif Input.is_key_clicked(pygame.K_ESCAPE):
            from game.scenes.main_menu_scene import MainMenuScene
            Logger.info("[GameScene] Returning to Main Menu.")
            self.scene_manager.change_scene(MainMenuScene())
    def _export_game(self) -> None:
        from engine.utils.serialization import serialize_game_state
        try:
            project_root = Path(__file__).resolve().parent.parent.parent
            saves_dir = project_root / "saves"
            saves_dir.mkdir(exist_ok=True)
            state = self.game.get_state()
            data = serialize_game_state(state)
            import time
            filename = f"export_{int(time.time())}.json"
            filepath = saves_dir / filename
            filepath.write_text(data, encoding="utf-8")
            self.hint_message = f"Exported: {filename}"
            self.hint_timer = 2.0
            Logger.info(f"[GameScene] Game exported to {filepath}")
        except Exception as exc:
            self.hint_message = "Export failed"
            self.hint_timer = 2.0
            Logger.error(f"[GameScene] Export error: {exc}")
    def render(self) -> None:
        self.game.render()
        if hasattr(self.renderer, "draw_text"):
            hud_text = "[Ctrl+Z] Undo  [Ctrl+Y] Redo  [H] Hint  [Q] Resign  [R] Reset  [Esc] Menu"
            try:
                self.renderer.draw_text(hud_text, (20, 15), size=18, color=(180, 190, 205))
            except TypeError:
                self.renderer.draw_text(hud_text, (20, 15), size=18)
            if (not self.game.is_game_over() and getattr(self.game, "game_mode", None) != GameMode.AI_VS_AI):
                if self.turn_timer > 15.0:
                    time_color = (80, 225, 125)
                elif self.turn_timer > 5.0:
                    time_color = (255, 210, 50)
                else:
                    time_color = (255, 75, 75)
                timer_str = f"Time: {self.turn_timer:.1f}s"
                try:
                    self.renderer.draw_text(timer_str, (1140, 15), size=20, color=time_color)
                except TypeError:
                    self.renderer.draw_text(timer_str, (1140, 15), size=20)
            ai_controller = getattr(self.game, "ai", None)
            if ai_controller and getattr(ai_controller, "is_thinking", False):
                try:
                    self.renderer.draw_text("AI Thinking...", (560, 15), size=20, color=(120, 200, 255))
                except TypeError:
                    self.renderer.draw_text("AI Thinking...", (560, 15), size=20)
            if self.hint_message:
                try:
                    self.renderer.draw_text(self.hint_message, (20, 45), size=22, color=(255, 215, 0))
                except TypeError:
                    self.renderer.draw_text(self.hint_message, (20, 45), size=22)