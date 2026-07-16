import pygame

from circleshape import CircleShape
from constants import CIRCLE_LIMIT_RADIUS, LINE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT


class CircleLimit(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=CIRCLE_LIMIT_RADIUS)
        self.locked = False

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def contains(self, shape):
        distance = self.position.distance_to(shape.position)
        return distance + shape.radius <= self.radius

    def is_outside(self, shape):
        return not self.contains(shape)

    def has_escaped(self, shape):
        """True solo cuando 'shape' ya PASÓ por completo el límite (los dos
        círculos ya ni se tocan), no apenas cuando toca o cruza el borde."""
        distance = self.position.distance_to(shape.position)
        return distance - shape.radius > self.radius

    def move_with_input(self, dt, keys, speed, max_y):
        """Fase de posicionamiento: el jugador mueve circle_limit con WASD.
        No puede salir de los bordes de la ventana."""
        if self.locked:
            return

        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1

        if direction.length() > 0:
            direction = direction.normalize()

        self.position += direction * speed * dt

        self.position.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.position.x))
        self.position.y = max(self.radius, min(max_y - self.radius, self.position.y),
)
