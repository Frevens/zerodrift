SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

FISH_RADIUS = 20
LINE_WIDTH = 2
FLOATER_RADIUS = 8
CIRCLE_LIMIT_RADIUS = 120

# --- Fish: velocidad variable ---
FISH_MIN_SPEED = 10
FISH_MAX_SPEED = 80
FISH_ACCEL = 60  # px/seg^2 -> qué tan rápido converge la velocidad actual a la velocidad objetivo

# Cada cuánto el fish decide un nuevo ángulo/velocidad "al azar" (da el efecto errático)
FISH_TURN_INTERVAL_MIN = 0.25
FISH_TURN_INTERVAL_MAX = 0.9

# Si la distancia de fish al BORDE de circle_limit es menor a esto, el próximo giro
# al azar se acota a un arco de EDGE_BIAS_ANGLE grados (en vez de 360), sesgado
# hacia alejarse del centro (achicar la distancia al borde).
EDGE_DISTANCE_THRESHOLD = 20
EDGE_BIAS_ANGLE = 120

# --- Floater ---
FLOATER_SPEED = 60

# --- CircleLimit (fase de posicionamiento previa al juego) ---
CIRCLE_LIMIT_SPEED = 220

# --- Rod (decorativo: A/D rota, W/S extiende/retrae) ---
ROD_MIN_LENGTH = 60
ROD_MAX_LENGTH = 220
ROD_TURN_SPEED = 90    # grados/seg
ROD_LENGTH_SPEED = 150  # px/seg
ROD_MAX_ANGLE = 110

# --- Partida ---
GAME_DURATION = 20.0     # segundos que hay que aguantar dentro de circle_limit para ganar
MIN_BITE_TIME = 1.0      # espera mínima random antes de que aparezca el pez
MAX_BITE_TIME = 4.0      # espera máxima random antes de que aparezca el pez
CAST_DURATION = 0.6      # duración de la animación de lanzamiento (rod -> centro de circle_limit)
