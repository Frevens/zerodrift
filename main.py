import random

import pygame

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CIRCLE_LIMIT_SPEED,
    CAST_DURATION,
    MIN_BITE_TIME,
    MAX_BITE_TIME,
    GAME_DURATION,
)
from logger import log_state, log_event
from rod import Rod
from fish import Fish
from floater import Floater, get_input_direction
from circle_limit import CircleLimit
from sticky_man import StickyMan
from background import Background

# --- Estados del juego ---
POSITIONING = "positioning"   # jugador mueve circle_limit con WASD, confirma con SPACE
CASTING = "casting"           # animación: floater viaja del rod al centro de circle_limit
WAITING_BITE = "waiting_bite"  # espera random antes de que aparezca el fish
PLAYING = "playing"           # tira y afloja: WASD modula la velocidad del fish
WON = "won"
LOST = "lost"


def make_fish(floater):
    """El fish aparece con ángulo random, con su boca coincidiendo con el
    círculo del floater (spawnea en la posición actual del floater)."""
    angle = random.uniform(0, 360)
    return Fish(floater.position.x, floater.position.y, rotation=angle)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zero Drift")
    print(f"Starting Zero Drift with pygame version: {pygame.version.ver}")
    print(f"Screen size set to: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0.0

    font = pygame.font.SysFont(None, 56)
    small_font = pygame.font.SysFont(None, 28)

    drawable = pygame.sprite.Group()

    Fish.containers = (drawable,)       # el update de Fish se llama a mano (necesita args extra)
    Floater.containers = (drawable,)    # ídem
    CircleLimit.containers = (drawable,)
    Rod.containers = (drawable,)
    StickyMan.containers = (drawable,)

    background = Background(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_HEIGHT - 90,
    )



    sticky_man = StickyMan(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT - 25,
    )

    def reset_round():
        circle_limit = CircleLimit(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
        )

        rod = Rod(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 50,
        )

        floater = Floater(
            rod.tip_position().x,
            rod.tip_position().y,
        )

        rod.floater = floater

        return circle_limit, rod, floater

    circle_limit, rod, floater = reset_round()

    sticky_man.rod = rod
    fish = None
    state = POSITIONING
    state_timer = 0.0
    bite_wait = 0.0
    cast_start_pos = pygame.Vector2(floater.position)
    game_time_left = GAME_DURATION
    result_message = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if state == POSITIONING and event.key == pygame.K_SPACE:
                    circle_limit.locked = True
                    state = CASTING
                    state_timer = 0.0
                    cast_start_pos = pygame.Vector2(floater.position)

                elif state in (WON, LOST) and event.key == pygame.K_RETURN:
                    for sprite in list(drawable):
                        sprite.kill()
                    circle_limit, rod, floater = reset_round()
                    fish = None
                    state = POSITIONING
                    state_timer = 0.0

        keys = pygame.key.get_pressed()
        background.update(dt)
        # El rod es puramente decorativo, pero mantiene sus propios
        # controles (A/D rota, W/S extiende/retrae) en todo momento.
        rod.handle_input(keys, dt)

        # --- UPDATE por estado ---
        if state == POSITIONING:
            floater.position = rod.tip_position()
            circle_limit.move_with_input(
                dt,
                keys,
                CIRCLE_LIMIT_SPEED,
                background.shoreline_y,
            )

        elif state == CASTING:
            state_timer += dt
            t = min(1.0, state_timer / CAST_DURATION)
            floater.position = cast_start_pos.lerp(circle_limit.position, t)
            if t >= 1.0:
                state = WAITING_BITE
                state_timer = 0.0
                bite_wait = random.uniform(MIN_BITE_TIME, MAX_BITE_TIME)

        elif state == WAITING_BITE:
            state_timer += dt
            if state_timer >= bite_wait:
                fish = make_fish(floater)
                state = PLAYING
                game_time_left = GAME_DURATION

        elif state == PLAYING:
            player_direction = get_input_direction(keys)

            fish.update(dt, player_direction, circle_limit)
            floater.follow(fish.position, circle_limit)

            game_time_left -= dt

            if circle_limit.has_escaped(fish):
                state = LOST
                result_message = "¡El pez escapó!"
                log_event("fish_escaped", position=list(fish.position))
            elif game_time_left <= 0:
                state = WON
                result_message = "¡Atrapaste al pez!"
                log_event("fish_caught")

        log_state()

        # --- DRAW ---
        screen.fill("black")
        background.draw(screen)
        StickyMan.draw(sticky_man, screen)
        rod.draw(screen)
        circle_limit.draw(screen)
        floater.draw(screen)
        if fish is not None and state in (PLAYING, WON, LOST):
            fish.draw(screen)

        if state == POSITIONING:
            txt = small_font.render(
                "WASD: mover el límite | SPACE: confirmar posición", True, "white"
            )
            screen.blit(txt, (20, 20))

        elif state == WAITING_BITE:
            txt = small_font.render("Esperando que pique...", True, "white")
            screen.blit(txt, (20, 20))

        elif state == PLAYING:
            txt = small_font.render(
                f"Tiempo restante: {max(0.0, game_time_left):.1f}s", True, "white"
            )
            screen.blit(txt, (20, 20))

        elif state in (WON, LOST):
            txt = font.render(result_message, True, "white")
            rect = txt.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(txt, rect)
            txt2 = small_font.render("Presiona ENTER para reintentar", True, "white")
            rect2 = txt2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
            screen.blit(txt2, rect2)

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

    pygame.quit()


if __name__ == "__main__":
    main()
