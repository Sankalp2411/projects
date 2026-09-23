# engine/ai/random_ai.py
from __future__ import annotations
import random
from typing import Any
class RandomAI:
    @staticmethod
    def select(legal_moves: list[Any]) -> Any | None:
        if not legal_moves:
            return None
        return random.choice(legal_moves)
    @staticmethod
    def select_weighted(legal_moves: list[Any],weights: list[float],) -> Any | None:
        if not legal_moves or not weights:
            return None
        if len(legal_moves) != len(weights):
            return random.choice(legal_moves)
        total = sum(weights)
        if total <= 0:
            return random.choice(legal_moves)
        return random.choices(legal_moves, weights=weights, k=1)[0]
    @staticmethod
    def add_noise(scores: list[float],noise_level: float = 0.3,) -> list[float]:
        if not scores:
            return scores
        score_range = max(scores) - min(scores) if len(scores) > 1 else 1.0
        if score_range == 0:
            score_range = 1.0
        sigma = noise_level * score_range
        return [s + random.gauss(0, sigma) for s in scores]