import pygame
import random
import math

# --------------------
# INIT
# --------------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()

# --------------------
# COLORS
# --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FIRE_COLORS = [(255, 200, 50), (255, 140, 0), (255, 60, 0)]  # yellow → orange → red

# --------------------
# PLAYER
# --------------------
player_width, player_height = 50, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 70
player_speed = 6

# --------------------
# BULLETS
# --------------------
bullets = []
bullet_speed = 8

# --------------------
# ENEMIES
# --------------------
enemies = []
enemy_speed = 3
spawn_timer = 0

# --------------------
# SCORE
# --------------------
score = 0
font = pygame.font.SysFont(None, 36)

# --------------------
# EXPLOSIONS
# --------------------
explosions = []

class Explosion:
    def __init__(self, x, y):
        self.particles = []
        for _ in range(25):  # more particles for bigger explosion
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            life = random.randint(20, 40)
            self.particles.append({
                "x": x,
                "y": y,
                "vx": speed * math.cos(angle),
                "vy": speed * math.sin(angle),
                "life": life,
                "max_life": life,
                "radius": random.randint(3, 6)
            })

    def update(self):
        """
        Updates particle positions and reduces life
        """
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15  # gravity
            p["life"] -= 1
            p["radius"] = max(0, p["radius"] - 0.1)

        # Remove dead particles
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, surface):
        """
        Draws the particles on the given surface
        """
        for p in self.particles:
            life_ratio = p["life"] / p["max_life"]
            if life_ratio >= 0.66:
                color = FIRE_COLORS[0]
            elif life_ratio >= 0.33:
                color = FIRE_COLORS[1]
            else:
                color = FIRE_COLORS[2]

            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), int(p["radius"]))

    def is_dead(self):
        """
        Returns True if all particles are dead
        """
        return len(self.particles) == 0
