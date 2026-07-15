import pygame

from constants import LINE_WIDTH, ROD_LENGTH


class Rod(pygame.sprite.Sprite):
    """Elemento puramente decorativo: no tiene input propio, solo sigue
    visualmente al floater (simula al jugador pescando)."""

    def __init__(self, base_x, base_y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.base = pygame.Vector2(base_x, base_y)
        self.floater = None

    def pole_tip(self):
        if self.floater is not None:
            direction = self.floater.visible_position() - self.base
            if direction.length() > 0:
                direction = direction.normalize()
            else:
                direction = pygame.Vector2(0, -1)
        else:
            direction = pygame.Vector2(0, -1)
        return self.base + direction * ROD_LENGTH

    def update(self, dt):
        pass  # decorativo, no tiene lógica propia

    def draw(self, screen):
        tip = self.pole_tip()
        pygame.draw.line(screen, "saddlebrown", self.base, tip, LINE_WIDTH * 2)
        if self.floater is not None:
            pygame.draw.line(screen, "white", tip, self.floater.visible_position(), LINE_WIDTH)
