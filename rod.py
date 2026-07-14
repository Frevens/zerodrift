import pygame
from constants import (
    LINE_WIDTH,
    ROD_LENGTH,
    ROD_MIN_LENGTH,
    ROD_LENGTH_SPEED,
    ROD_TURN_SPEED,
    ROD_SWING_AMPLITUDE,
)


class Rod(pygame.sprite.Sprite):
    def __init__(self, base_x, base_y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.base = pygame.Vector2(base_x, base_y)
        self.rotation = 0
        self.length = (ROD_LENGTH + ROD_MIN_LENGTH) / 2
        self.floater = None

    def handle_input(self, dt, keys):
        if keys[pygame.K_a]:
            self.rotation -= ROD_TURN_SPEED * dt
        if keys[pygame.K_d]:
            self.rotation += ROD_TURN_SPEED * dt

        self.rotation = max(
            -ROD_SWING_AMPLITUDE,
            min(ROD_SWING_AMPLITUDE, self.rotation),
        )

        if keys[pygame.K_w]:
            self.length += ROD_LENGTH_SPEED * dt

        if keys[pygame.K_s]:
            self.length -= ROD_LENGTH_SPEED * dt

        self.length = max(
            ROD_MIN_LENGTH,
            min(ROD_LENGTH, self.length),
        )

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.handle_input(dt, keys)

    def tip_position(self):
        direction = pygame.Vector2(0, -1).rotate(self.rotation)
        return self.base + direction * self.length

    def draw(self, screen):
        # Dibuja la línea de pesca si existe un flotador
        if self.floater is not None:
            pygame.draw.line(
                screen,
                "white",
                self.tip_position(),
                self.floater.visible_position(),
                LINE_WIDTH,
            )

        # Dibuja la caña
        pygame.draw.line(
            screen,
            "white",
            self.base,
            self.tip_position(),
            LINE_WIDTH * 2,
        )