# Zero Drift

Zero Drift is a first personal project built as part of the boot.dev curriculum, following the same Python + pygame track used in the course's Asteroids project.

## About the game

Zero Drift is a simple 2D top-down fishing game built around two concentric circles sharing the same center:

- **CircleLimit** is the maximum reach of the fishing line. It's fixed and never moves.
- **Fish** constantly tries to drift away from the center, out toward (and past) that limit.

The player's job is to keep the fish from breaking free, by reacting to its movement. Controls are `WASD`, which rotate the fishing rod left and right.

The other pieces on screen:

- **Floater** sits on top of the fish while the fish is within the line's reach, moving together with it. Once the fish reaches the edge of CircleLimit, the floater gets pinned there and can't go any further.
- **Line** is just a straight line rendered from the tip of the rod to the floater's center — it has no state of its own, it's purely visual.
- **Rod** pivots around its base, rotating within a 120° range in response to `A`/`D` input. It only rotates (no separate "raise the rod" animation) to keep things simple.

**Escape condition:** while the fish is inside CircleLimit, it and the floater move together. Once the fish crosses CircleLimit, the floater stays pinned at the edge — if the fish then drifts far enough that the distance between it and the pinned floater exceeds the fish's own radius, it has broken free from the line. That triggers a message and resets the casting animation.



## Project structure

Each class lives in its own file:

- `circle_limit.py` — `CircleLimit`
- `fish.py` — `Fish`
- `floater.py` — `Floater`
- `line.py` — `Line`
- `rod.py` — `Rod`

## Logging

This project reuses the `logger.py` module from the course's Asteroids project, with a small modification: the original version only recorded one standalone game object (outside of a `pygame.sprite.Group`) per snapshot. Since Zero Drift relies on several individual objects at once (CircleLimit, Fish, Floater), the logger was adjusted to record all of them on each snapshot instead of just the first one found.

The logger doesn't hardcode any class or variable names — it detects objects purely by their attributes (`position`, `velocity`, `radius`, `rotation`), so `Line` and `Rod` (which don't expose a `position`) are naturally left out of the state log.

- `game_state.jsonl` — periodic snapshots of object positions, velocities, radious, and rotations.
- `game_events.jsonl` — discrete events (e.g. the fish breaking free from the line).
