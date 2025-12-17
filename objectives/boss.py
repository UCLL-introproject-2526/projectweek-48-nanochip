import pygame
import os
import random

# --------------------------
# BOSS BULLET CLASS
# --------------------------
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a simple red bullet
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0)) # Red
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 5  # Moves down

    def update(self):
        self.rect.y += self.speed_y
        # Remove if it goes off screen
        if self.rect.top > 1000: 
            self.kill()

# --------------------------
# BOSS CLASS
# --------------------------
class Boss(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        
        # 1. SETUP IMAGE
        # Default to a big Red Square (Fallback if image fails)
        self.width = 100
        self.height = 80
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 0, 0)) # Dark Red
        
        # Try to load a real image if it exists
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Looks for 'enemy_ship.png' in objectives/images/
            img_path = os.path.join(base_dir, "images", "enemy_ship.png") 
            if os.path.exists(img_path):
                loaded_img = pygame.image.load(img_path).convert_alpha()
                self.image = pygame.transform.scale(loaded_img, (self.width, self.height))
        except Exception as e:
            print(f"Warning: Could not load Boss image. Using square. {e}")

        # 2. SETUP POSITION
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.y = 50 # Start near top
        self.screen_width = screen_width

        # 3. MOVEMENT & STATS
        self.speed_x = 3
        self.max_hp = 500
        self.hp = self.max_hp
        
        # 4. SHOOTING SETUP
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 1000  # Shoots every 1 second

    def update(self):
        # MOVE: Bounce left and right
        self.rect.x += self.speed_x
        
        # Bounce off walls
        if self.rect.right >= self.screen_width:
            self.speed_x = -3 # Go Left
        elif self.rect.left <= 0:
            self.speed_x = 3  # Go Right

        # SHOOT: Check timer
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = now

    def shoot(self):
        # Create a bullet at the bottom center of the boss
        bullet = BossBullet(self.rect.centerx, self.rect.bottom)
        self.bullets.add(bullet)