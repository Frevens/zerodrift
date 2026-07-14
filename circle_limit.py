import pygame
from circleshape import CircleShape
from constants import CIRCLE_LIMIT_RADIUS, LINE_WIDTH

class CircleLimit(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=CIRCLE_LIMIT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def contains(self, shape):
        distance = self.position.distance_to(shape.position)
        return distance + shape.radius <= self.radius

    def is_outside(self, shape):
        return not self.contains(shape)