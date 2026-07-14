import pygame
from circleshape import CircleShape
from constants import FLOATER_RADIUS, FISH_RADIUS, FLOATER_SPEED


class Floater(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=FLOATER_RADIUS)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0

    def visible_position(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        return self.position + forward * FISH_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.visible_position(), self.radius, 0)

    def handle_input(self, keys):
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

        self.velocity = direction * FLOATER_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.handle_input(keys)

        self.position += self.velocity * dt