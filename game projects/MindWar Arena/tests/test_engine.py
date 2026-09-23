"""Unit tests for core engine components: EventManager, StateManager, and GameBase."""

import time

from engine.ai_base import AIBase
from engine.core.event_manager import EventManager
from engine.core.state_manager import MoveRecord, StateManager
from engine.game_base import GameBase
from engine.utils.constants import Difficulty, EventType, GameMode, GameState


def test_event_manager_subscribe_emit():
    em = EventManager()
    calls = []

    def on_move(move=None, player=None):
        calls.append((move, player))

    em.subscribe(EventType.ON_MOVE_MADE, on_move)
    em.emit(EventType.ON_MOVE_MADE, move=(0, 0), player=1)

    assert len(calls) == 1
    assert calls[0] == ((0, 0), 1)

    # Test unsubscribe
    em.unsubscribe(EventType.ON_MOVE_MADE, on_move)
    em.emit(EventType.ON_MOVE_MADE, move=(1, 1), player=2)
    assert len(calls) == 1


def test_state_manager_undo_redo():
    sm = StateManager(max_history=5)
    assert not sm.can_undo()
    assert not sm.can_redo()

    record1 = MoveRecord(move=(0, 0), player=1)
    record2 = MoveRecord(move=(1, 1), player=2)
    sm.push(record1)
    sm.push(record2)

    assert sm.can_undo()
    assert sm.move_count == 2

    # Undo
    popped = sm.undo()
    assert popped == record2
    assert sm.can_redo()
    assert sm.move_count == 1

    # Redo
    redone = sm.redo()
    assert redone == record2
    assert sm.move_count == 2
    assert not sm.can_redo()


def test_game_base_lifecycle():
    class DummyRenderer:
        pass

    game = GameBase(renderer=DummyRenderer(), game_mode=GameMode.HUMAN_VS_HUMAN)
    assert game.game_state == GameState.NOT_STARTED
    assert game.current_player == 1

    game.initialize()
    assert game.game_state == GameState.RUNNING

    # Player alternation
    p1 = game.choose_starting_player()
    p2 = game.choose_starting_player()
    assert p1 != p2


def test_ai_async_non_blocking_execution():
    class SlowAI(AIBase):
        def _select_beginner_move(self, game_state, legal_moves):
            time.sleep(0.05)  # Simulate search
            return legal_moves[0]

    class MockGame:
        def is_game_over(self):
            return False

        def get_state(self):
            return {"legal_moves": [(0, 0), (0, 1)]}

    ai = SlowAI(player=2, difficulty=Difficulty.BEGINNER, is_async=True)
    game = MockGame()

    # Call 1: starts background search, immediately returns None (non-blocking!)
    action = ai.get_action(game)
    assert action is None
    assert ai.is_thinking is True

    # Wait for thread to finish
    time.sleep(0.1)

    # Call 2: retrieves computed move from worker thread
    move = ai.get_action(game)
    assert move == (0, 0)
    assert ai.is_thinking is False
