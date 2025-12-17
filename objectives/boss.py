import pygame
import random

# 1. Define the Boss Bullet Class
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a simple red bullet (or load an image if you have one)
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0)) # Red color for enemy fire
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 5  # Speed moving down

    def update(self):
        self.rect.y += self.speed_y
        # Remove if it goes off screen
        if self.rect.top > 800: # Assuming height is 600 or 800
            self.kill()

# 2. Update your Boss Class
class Boss(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        # ... (keep your existing image loading code here) ...
        
        # Add these variables for shooting:
        self.bullets = pygame.sprite.Group() # Group to hold boss bullets
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 1000  # Boss shoots every 1000ms (1 second)

    def update(self):
        # ... (keep your existing movement code here) ...

        # SHOOTING LOGIC
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = now
            
    def shoot(self):
        # Create a bullet at the boss's center
        bullet = BossBullet(self.rect.centerx, self.rect.bottom)
        self.bullets.add(bullet)