import pygame
import random
from objectives.explosion import Explosion

class Boss:
    def __init__(self, x, y, width, height, hp, level):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_hp = hp
        self.hp = hp
        self.level = level
        self.speed = 2
        self.direction = 1  # left/right movement
        self.shoot_timer = 0
        self.shoot_cooldown = max(60 - level*2, 20)  # faster shooting at higher levels

    def update(self, enemy_bullets):
        # Move left/right
        self.rect.x += self.speed * self.direction
        if self.rect.right > 800 or self.rect.left < 0:
            self.direction *= -1

        # Shoot bullets
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_cooldown:
            bullet = pygame.Rect(self.rect.centerx - 5, self.rect.bottom, 10, 15)
            enemy_bullets.append(bullet)
            self.shoot_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 0, 200), self.rect)  # purple boss
        # Draw HP bar
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 10, int(self.rect.width * hp_ratio), 5))
