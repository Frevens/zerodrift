import pygame

from circleshape import CircleShape
from constants import FLOATER_RADIUS


def get_input_direction(keys):
    """Vector de dirección normalizado según WASD estándar
    (W: arriba, A: izquierda, S: abajo, D: derecha)."""
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
    return direction


class Floater(CircleShape):
    """El floater queda 'mordido' por el fish: mientras el fish está dentro
    de circle_limit, el floater sigue exactamente su posición. El floater
    nunca puede superar circle_limit (a diferencia del fish, que sí puede
    escaparse); si el fish se aleja más allá del límite, el floater se queda
    clavado en el borde, en la dirección del fish, sin seguirlo más allá."""

    def __init__(self, x, y):
        super().__init__(x, y, radius=FLOATER_RADIUS)
        self.velocity = pygame.Vector2(0, 0)

    def visible_position(self):
        return self.position

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.visible_position(), self.radius, 0)

    def clamp_to(self, circle_limit):
        """Floater no puede superar circle_limit."""
        offset = self.position - circle_limit.position
        max_dist = circle_limit.radius - self.radius
        if max_dist > 0 and offset.length() > max_dist:
            self.position = circle_limit.position + offset.normalize() * max_dist

    def follow(self, target_position, circle_limit):
        """Sigue la posición del fish (mordida), clampeado a circle_limit."""
        self.position = pygame.Vector2(target_position)
        self.clamp_to(circle_limit)
