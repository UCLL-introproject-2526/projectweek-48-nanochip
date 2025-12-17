import pygame
import random

# Power-up types
EXTRA_LIFE = "life"
RAPID_FIRE = "rapid"
SHIELD = "shield"

POWERUP_COLORS = {
    EXTRA_LIFE: (0, 255, 0),
    RAPID_FIRE: (0, 200, 255),
    SHIELD: (255, 255, 0),
}

class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = type
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, POWERUP_COLORS[self.type], self.rect)

# Spawn power-up at enemy position
def spawn_powerup_at(powerups, x, y):
    if random.random() < 0.15:  # 15% drop chance
        type = random.choice([EXTRA_LIFE, RAPID_FIRE, SHIELD])
        powerups.append(PowerUp(x, y, type))
