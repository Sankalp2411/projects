"""Unit tests for AI components: MinimaxEngine and TranspositionTable."""

from engine.ai.minimax import MinimaxEngine
from engine.ai.random_ai import RandomAI
from engine.ai.transposition_table import TranspositionTable, TTFlag


def test_transposition_table_store_and_probe():
    tt = TranspositionTable(size_mb=1)
    tt.clear()

    key = 123456789
    tt.store(hash_key=key, depth=4, score=15.5, flag=TTFlag.EXACT, best_move=(1, 2))

    entry = tt.probe(hash_key=key)
    assert entry is not None
    assert entry.score == 15.5
    assert entry.depth == 4
    assert entry.flag == TTFlag.EXACT
    assert entry.best_move == (1, 2)


def test_random_ai():
    legal_moves = [(0, 0), (1, 1), (2, 2)]
    move = RandomAI.select(legal_moves)
    assert move in legal_moves

    # Empty moves returns None
    assert RandomAI.select([]) is None


def test_minimax_engine_basic_search():
    # Simple game tree: tree of numbers where maximizer wants highest number
    class MockTreeState:
        def __init__(self, value, is_leaf=False, children=None):
            self.value = value
            self.is_leaf = is_leaf
            self.children = children or []

    def get_moves(state):
        return list(range(len(state.children)))

    def apply_move(state, move_idx):
        return state.children[move_idx]

    def evaluate(state):
        return float(state.value)

    def is_terminal(state):
        return state.is_leaf

    # Leaf nodes with values 3, 5, 2, 9
    leaf1 = MockTreeState(3, is_leaf=True)
    leaf2 = MockTreeState(5, is_leaf=True)
    leaf3 = MockTreeState(2, is_leaf=True)
    leaf4 = MockTreeState(9, is_leaf=True)

    mid1 = MockTreeState(0, children=[leaf1, leaf2])
    mid2 = MockTreeState(0, children=[leaf3, leaf4])
    root = MockTreeState(0, children=[mid1, mid2])

    engine = MinimaxEngine(
        get_moves=get_moves,
        apply_move=apply_move,
        evaluate=evaluate,
        is_terminal=is_terminal,
    )

    best_move = engine.search(root, depth=2)
    assert best_move in [0, 1]
