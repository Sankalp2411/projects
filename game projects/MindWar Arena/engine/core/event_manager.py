# engine/core/event_manager.py
from __future__ import annotations
import logging
from collections import defaultdict
from collections.abc import Callable
from typing import Any
from engine.utils.constants import EventType
logger = logging.getLogger(__name__)
Listener = Callable[..., None]
class EventManager:
    def __init__(self) -> None:
        self._listeners: dict[EventType, list[Listener]] = defaultdict(list)
        self._muted: set[EventType] = set()
        self._paused: bool = False
    def subscribe(self,event_type: EventType,callback: Listener,) -> None:
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)
    def unsubscribe(self,event_type: EventType,callback: Listener,) -> None:
        try:
            self._listeners[event_type].remove(callback)
        except ValueError:
            pass
    def unsubscribe_all(self,event_type: EventType | None = None,) -> None:
        if event_type is None:
            self._listeners.clear()
        else:
            self._listeners[event_type].clear()
    def emit(self, event_type: EventType, **kwargs: Any) -> None:
        if self._paused:
            return
        if event_type in self._muted:
            return
        for callback in list(self._listeners.get(event_type, [])):
            try:
                callback(**kwargs)
            except Exception:
                logger.exception("Error in event listener %s for %s",callback,event_type,)
    def mute(self, event_type: EventType) -> None:
        self._muted.add(event_type)
    def unmute(self, event_type: EventType) -> None:
        self._muted.discard(event_type)
    def pause(self) -> None:
        self._paused = True
    def resume(self) -> None:
        self._paused = False
    def has_listeners(self, event_type: EventType) -> bool:
        return bool(self._listeners.get(event_type))
    def listener_count(self, event_type: EventType) -> int:
        return len(self._listeners.get(event_type, []))
_global_event_manager: EventManager | None = None
def get_event_manager() -> EventManager:
    global _global_event_manager
    if _global_event_manager is None:
        _global_event_manager = EventManager()
    return _global_event_manager
def reset_event_manager(replacement: EventManager | None = None) -> None:
    global _global_event_manager
    if _global_event_manager is not None:
        _global_event_manager.unsubscribe_all()
    _global_event_manager = replacement