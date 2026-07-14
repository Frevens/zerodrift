import pygame
import random
from circleshape import CircleShape
from constants import (
    LINE_WIDTH, FISH_RADIUS,
    FISH_MIN_SPEED, FISH_MAX_SPEED, FISH_ACCEL, FISH_TURN_SPEED,
    OPPOSITION_FORCE,
)
from logger import log_event

class Fish(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, FISH_RADIUS)
        self.rotation = 0
        self.speed = (FISH_MIN_SPEED + FISH_MAX_SPEED) / 2  # arranca a mitad de velocidad
        self.velocity = pygame.Vector2(0, 0)

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

    def update(self, dt, floater):
        # --- TODO: reemplazar por la IA real de fish ---
        self.rotation += random.uniform(-1, 1) * FISH_TURN_SPEED * dt
        self.speed += random.uniform(-1, 1) * FISH_ACCEL * dt
        self.speed = max(FISH_MIN_SPEED, min(FISH_MAX_SPEED, self.speed))
        # -------------------------------------------------

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity = forward * self.speed

        # oposición directa: floater "tira" de fish hacia su posición
        to_floater = floater.position - self.position
        if to_floater.length() > 0:
            pull = to_floater.normalize() * OPPOSITION_FORCE
            self.velocity += pull * dt

        self.position += self.velocity * dt