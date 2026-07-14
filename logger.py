import inspect
import json
import math
from datetime import datetime
from typing import NotRequired, TypedDict

class SpriteInfo(TypedDict):
    type: str
    pos: NotRequired[list[float]]
    vel: NotRequired[list[float]]
    rad: NotRequired[float]
    rot: NotRequired[float]


class GroupInfo(TypedDict):
    count: int
    sprites: list[SpriteInfo]


__all__ = ["log_state", "log_event"]

_FPS = 60
_MAX_SECONDS = 16
_SPRITE_SAMPLE_LIMIT = 10  # Maximum number of sprites to log per group

_frame_count = 0
_state_log_initialized = False
_event_log_initialized = False
_start_time = datetime.now()


def _build_sprite_info(sprite: object) -> SpriteInfo:
    sprite_info: SpriteInfo = {"type": sprite.__class__.__name__}

    if hasattr(sprite, "position"):
        sprite_info["pos"] = [
            round(sprite.position.x, 2),
            round(sprite.position.y, 2),
        ]

    if hasattr(sprite, "velocity"):
        sprite_info["vel"] = [
            round(sprite.velocity.x, 2),
            round(sprite.velocity.y, 2),
        ]

    if hasattr(sprite, "radius"):
        sprite_info["rad"] = sprite.radius

    if hasattr(sprite, "rotation"):
        sprite_info["rot"] = round(sprite.rotation, 2)

    return sprite_info


def log_state() -> None:
    global _frame_count, _state_log_initialized

    # Stop logging after `_MAX_SECONDS` seconds
    if _frame_count > _FPS * _MAX_SECONDS:
        return

    # Take a snapshot approx. once per second
    _frame_count += 1
    if _frame_count % _FPS != 0:
        return

    now = datetime.now()

    frame = inspect.currentframe()
    if frame is None:
        return

    frame_back = frame.f_back
    if frame_back is None:
        return

    local_vars = frame_back.f_locals.copy()

    screen_size: list[int] = []
    game_state: dict[str, object] = {}

    for key, value in local_vars.items():
        # 1) pygame screen/surface -> just grab its size
        if "pygame" in str(type(value)) and hasattr(value, "get_size"):
            screen_size = list(value.get_size())
            continue

        # 2) pygame.sprite.Group (or similar) -> sample sprites inside it
        if hasattr(value, "__class__") and "Group" in value.__class__.__name__:
            sprites_data: list[SpriteInfo] = []

            for i, sprite in enumerate(value):
                if i >= _SPRITE_SAMPLE_LIMIT:
                    break
                sprites_data.append(_build_sprite_info(sprite))

            game_state[key] = {"count": len(value), "sprites": sprites_data}
            continue

        # 3) any standalone object with a `position` (boundary circle, escaping
        # circle, float, etc.) -> log ALL of them, not just the first.
        # This is the fix vs. the original Asteroids logger, which stopped
        # after the first one because it only tracked a single `player`.
        if hasattr(value, "position"):
            game_state[key] = _build_sprite_info(value)

    entry: dict[str, object] = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "screen_size": screen_size,
        **game_state,
    }

    # New log file on each run
    mode = "w" if not _state_log_initialized else "a"
    with open("game_state.jsonl", mode) as f:
        f.write(json.dumps(entry) + "\n")

    _state_log_initialized = True


def log_event(event_type: str, **details: object) -> None:
    global _event_log_initialized

    now = datetime.now()

    event: dict[str, object] = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
        "elapsed_s": math.floor((now - _start_time).total_seconds()),
        "frame": _frame_count,
        "type": event_type,
        **details,
    }

    mode = "w" if not _event_log_initialized else "a"
    with open("game_events.jsonl", mode) as f:
        f.write(json.dumps(event) + "\n")

    _event_log_initialized = True
