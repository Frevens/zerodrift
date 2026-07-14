import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zero Drift")
    print(f"Starting Zero Drift with pygame version: {pygame.version.ver}")
    print(f"Screen size set to: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    # 1. Crea un reloj y una variable de tiempo delta dt.
    clock = pygame.time.Clock()  # Inicia el reloj
    dt = 0                       # Delta time en segundos

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        log_state()

        # Dibuja todo
        screen.fill("black")

        # (later you'll draw your game objects here)
        pygame.display.flip()

        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()