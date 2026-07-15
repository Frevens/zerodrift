import pygame
import random

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    FISH_RADIUS,
    FISH_MIN_SPEED,
    FISH_MAX_SPEED,
    FISH_ACCEL,
    FISH_TURN_INTERVAL_MIN,
    FISH_TURN_INTERVAL_MAX,
    EDGE_DISTANCE_THRESHOLD,
    EDGE_BIAS_ANGLE,
)


class Fish(CircleShape):
    def __init__(self, x, y, rotation=0):
        super().__init__(x, y, FISH_RADIUS)
        self.rotation = rotation
        self.speed = random.uniform(FISH_MIN_SPEED, FISH_MAX_SPEED)
        self.velocity = pygame.Vector2(0, 0)
        self._turn_timer = 0.0
        self._reset_turn_timer()

    def _reset_turn_timer(self):
        self._turn_timer = random.uniform(FISH_TURN_INTERVAL_MIN, FISH_TURN_INTERVAL_MAX)

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.fish_shape(), LINE_WIDTH)

    def fish_shape(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = forward.rotate(90)
        points_local = [
            (1.0, 0.0), (0.55, 0.35), (0.05, 0.55), (-0.45, 0.25),
            (-0.55, 0.55), (-0.35, 0.12), (-1.0, 0.0), (-0.35, -0.12),
            (-0.55, -0.55), (-0.45, -0.25), (0.05, -0.55), (0.55, -0.35),
        ]
        return [
            self.position + forward * f * self.radius + right * w * self.radius
            for f, w in points_local
        ]

    def _pick_new_direction(self, circle_limit):
        """Elige un nuevo ángulo al azar. Si el fish está a menos de
        EDGE_DISTANCE_THRESHOLD del BORDE de circle_limit, el nuevo ángulo se
        acota a un arco de EDGE_BIAS_ANGLE grados centrado en la dirección que
        se aleja del centro (achica la distancia al borde). Si no, gira libre
        en 360 grados."""
        to_fish = self.position - circle_limit.position
        distance_to_center = to_fish.length()
        distance_to_edge = circle_limit.radius - distance_to_center

        if distance_to_edge < EDGE_DISTANCE_THRESHOLD and distance_to_center > 0:
            outward_angle = pygame.Vector2(0, 1).angle_to(to_fish)
            spread = EDGE_BIAS_ANGLE / 2
            self.rotation = outward_angle + random.uniform(-spread, spread)
        else:
            self.rotation = random.uniform(0, 360)

        self.speed = random.uniform(FISH_MIN_SPEED, FISH_MAX_SPEED)

    def update(self, dt, player_direction, circle_limit):
        self._turn_timer -= dt
        if self._turn_timer <= 0:
            self._pick_new_direction(circle_limit)
            self._reset_turn_timer()

        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # El input del jugador modula la velocidad del fish: si las teclas
        # acompañan la dirección del fish, acelera hacia el máximo; si se
        # oponen, decelera hacia el mínimo.
        if player_direction.length() > 0:
            alignment = forward.normalize().dot(player_direction.normalize())
        else:
            alignment = 0.0

        target_speed = FISH_MIN_SPEED + (alignment + 1) / 2 * (FISH_MAX_SPEED - FISH_MIN_SPEED)

        if self.speed < target_speed:
            self.speed = min(target_speed, self.speed + FISH_ACCEL * dt)
        else:
            self.speed = max(target_speed, self.speed - FISH_ACCEL * dt)

        self.velocity = forward * self.speed
        self.position += self.velocity * dt
