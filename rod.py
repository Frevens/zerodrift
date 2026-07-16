import pygame

from constants import LINE_WIDTH, ROD_MIN_LENGTH, ROD_MAX_LENGTH, ROD_TURN_SPEED, ROD_LENGTH_SPEED, ROD_MAX_ANGLE


class Rod(pygame.sprite.Sprite):
    """Elemento puramente decorativo: no interviene en la mecánica del
    juego (fish / floater / circle_limit). Se controla con A/D (rota) y
    W/S (extiende/retrae), simulando al jugador moviendo la caña mientras
    pesca. La línea siempre conecta la punta de la caña con el floater,
    esté éste donde esté."""

    def __init__(self, base_x, base_y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.base = pygame.Vector2(base_x, base_y)
        self.rotation = 0.0  # 0 = apuntando hacia arriba
        self.length = ROD_MIN_LENGTH
        self.floater = None

    def handle_input(self, keys, dt):
        if keys[pygame.K_a]:
            self.rotation -= ROD_TURN_SPEED * dt
        if keys[pygame.K_d]:
            self.rotation += ROD_TURN_SPEED * dt
        if keys[pygame.K_w]:
            self.length = min(ROD_MAX_LENGTH, self.length + ROD_LENGTH_SPEED * dt)
        if keys[pygame.K_s]:
            self.length = max(ROD_MIN_LENGTH, self.length - ROD_LENGTH_SPEED * dt)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.handle_input(keys, dt)

    def tip_position(self):
        direction = pygame.Vector2(0, -1).rotate(self.rotation)
        return self.base + direction * self.length

    def draw(self, screen):
        tip = self.tip_position()
        pygame.draw.line(screen, "saddlebrown", self.base, tip, LINE_WIDTH * 2)
        if self.floater is not None:
            pygame.draw.line(screen, "white", tip, self.floater.visible_position(), LINE_WIDTH)
