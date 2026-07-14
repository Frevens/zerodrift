SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

FISH_RADIUS = 20
LINE_WIDTH = 2
FLOATER_RADIUS = 8
CIRCLE_LIMIT_RADIUS = 250

FLOATER_LEASH_RADIUS = 120   # pendiente de usar

# --- Fish: velocidad variable ---
FISH_MIN_SPEED = 0
FISH_MAX_SPEED = 80
FISH_ACCEL = 40          # px/seg^2 -> qué tan rápido cambia la velocidad (placeholder)
FISH_TURN_SPEED = 30     # grados/seg de giro autónomo (placeholder)
OPPOSITION_FORCE = 120

# --- Floater ---
FLOATER_SPEED = 58      # un poco más que la mitad de FISH_MAX_SPEED (80)

# --- Rod ---
ROD_LENGTH = 150         # largo máximo (rod "bajada")
ROD_MIN_LENGTH = 60      # largo mínimo (rod "levantada")
ROD_LENGTH_SPEED = 100   # px/seg al cambiar largo con W/S
ROD_TURN_SPEED = 90      # grados/seg al rotar con A/D
ROD_SWING_AMPLITUDE = 60 # límite de rotación hacia cada lado