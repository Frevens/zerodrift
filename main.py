import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from rod import Rod
from fish import Fish
from floater import Floater
from circle_limit import CircleLimit






def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zero Drift")
    print(f"Starting Zero Drift with pygame version: {pygame.version.ver}")
    print(f"Screen size set to: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    # 1. Crea un reloj y una variable de tiempo delta dt.
    clock = pygame.time.Clock()  # Inicia el reloj
    dt = 0.0                     # Delta time en segundos

    updatable = pygame.sprite.Group()  # Grupo de objetos que se actualizarán cada frame
    drawable = pygame.sprite.Group()    # Grupo de objetos que se dibujarán cada frame
    Fish.containers = (updatable, drawable)
    rod = pygame.sprite.Group()  # Grupo de objetos que se actualizarán cada frame
    Floater.containers = (rod, updatable, drawable)
    Rod.containers = (rod, updatable, drawable)
    CircleLimit.containers = (updatable, drawable)
    circle_limit = CircleLimit(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )

    rod = Rod(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT - 50,
    )
    floater = Floater(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    rod.floater = floater

    floater = Floater(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Lógica del juego va acá (usa dt para movimientos basados en tiempo (time-based movement)).
        # 🔹 UPDATE (lógica del juego)
        updatable.update(dt)        

        log_state()

        # Dibuja todo
        screen.fill("black")

        # Dibuja Player en cada cuadro. 
        for object in drawable:
            object.draw(screen)

        # (later you'll draw your game objects here)
        pygame.display.flip()

            # tick() regresa milisegundos desde la última llamada → convierte a segundos
        dt = clock.tick(60) / 1000.0






    pygame.quit()

if __name__ == "__main__":
    main()