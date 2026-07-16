import pygame


class StickyMan(pygame.sprite.Sprite):
    """Pescador visto desde arriba."""

    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.rod = None

    def update(self, dt):
        pass

    def draw(self, screen):
        body_color = "burlywood4"

        # Cabeza
        head_radius = 10
        head_center = pygame.Vector2(
            self.position.x,
            self.position.y - 5,
        )

        pygame.draw.circle(
            screen,
            body_color,
            (int(head_center.x), int(head_center.y)),
            head_radius,
        )

        # Hombros
        shoulder_y = self.position.y
        left_shoulder = pygame.Vector2(self.position.x - 18, shoulder_y)
        right_shoulder = pygame.Vector2(self.position.x + 18, shoulder_y)

        pygame.draw.line(
            screen,
            body_color,
            left_shoulder,
            right_shoulder,
            8,
        )

        if self.rod is not None:
            pygame.draw.line(
                screen,
                body_color,
                left_shoulder,
                self.rod.base,
                5,
            )

            pygame.draw.line(
                screen,
                body_color,
                right_shoulder,
                self.rod.base,
                5,
            )