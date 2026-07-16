import random
import pygame


class Background:
    def __init__(self, width, height, shoreline_y):
        self.width = width
        self.height = height
        self.shoreline_y = shoreline_y

        self.water_reflections = []
        self.grass = []

        self._generate_water()
        self._generate_grass()

    def _generate_water(self):
        """Genera pequeños reflejos horizontales sobre el agua."""
        for _ in range(180):
            self.water_reflections.append(
                {
                    "x": random.randint(0, self.width),
                    "y": random.randint(10, self.shoreline_y - 15),
                    "length": random.randint(6, 18),
                    "visible": random.choice([True, False]),
                    "timer": random.uniform(0.0, 1.5),
                }
            )

    def _generate_grass(self):
        """Genera mechones de pasto debajo de la costa."""
        for _ in range(250):
            self.grass.append(
                (
                    random.randint(0, self.width),
                    random.randint(self.shoreline_y + 5, self.height - 5),
                    random.randint(6, 12),
                )
            )

    def update(self, dt):
        """Hace parpadear algunos reflejos del agua."""
        for reflection in self.water_reflections:
            reflection["timer"] -= dt

            if reflection["timer"] <= 0:
                reflection["visible"] = not reflection["visible"]
                reflection["timer"] = random.uniform(0.2, 1.2)

    def draw(self, screen):
        # ---------- Agua ----------
        screen.fill((45, 120, 185))

        for r in self.water_reflections:
            if r["visible"]:
                pygame.draw.line(
                    screen,
                    (235, 245, 255),
                    (r["x"], r["y"]),
                    (r["x"] + r["length"], r["y"]),
                    2,
                )

        # ---------- Pasto ----------
        pygame.draw.rect(
            screen,
            (60, 140, 60),
            (
                0,
                self.shoreline_y,
                self.width,
                self.height - self.shoreline_y,
            ),
        )

        # ---------- Línea de costa ----------
        pygame.draw.line(
            screen,
            (150, 120, 70),
            (0, self.shoreline_y),
            (self.width, self.shoreline_y),
            3,
        )

        # ---------- Pasto ----------
        for x, y, h in self.grass:

            # Centro
            pygame.draw.line(
                screen,
                (20, 90, 20),
                (x, y),
                (x, y - h),
                1,
            )

            # Izquierda
            pygame.draw.line(
                screen,
                (20, 90, 20),
                (x, y),
                (x - 3, y - h + 2),
                1,
            )

            # Derecha
            pygame.draw.line(
                screen,
                (20, 90, 20),
                (x, y),
                (x + 3, y - h + 2),
                1,
            )