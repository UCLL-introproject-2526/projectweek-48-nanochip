import pygame
import os
import random

# --------------------------
# BOSS BULLET CLASS
# --------------------------
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx=0, dy=5, color=(255,0,0)):
        super().__init__()
        # Create a simple bullet
        self.image = pygame.Surface((10, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = dx
        self.speed_y = dy  # Moves down

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Remove if it goes off screen
        if self.rect.top > 1000 or self.rect.right < -200 or self.rect.left > 2000:
            self.kill()

# --------------------------
# BOSS CLASS
# --------------------------
class Boss(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, target_y=50, variant=None):
        super().__init__()
        self.variant = variant
        
        # 1. SETUP IMAGE
        # Default size (can be adjusted by variant)
        self.width = 100
        self.height = 80

        # Variant sizing: make the stronger/second boss a bit larger
        if self.variant in ("sotrak_rewop", "stark_rewop"):
            self.width = int(self.width * 2)
            self.height = int(self.height * 2)

        # Default image surface (fallback)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 0, 0)) # Dark Red
        
        # Try to load a real image if it exists
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Looks for 'alien_boss.png' in objectives/images/
            img_path = os.path.join(base_dir, "images", "alien_boss.png") 
            if os.path.exists(img_path):
                loaded_img = pygame.image.load(img_path).convert_alpha()
                self.image = pygame.transform.scale(loaded_img, (self.width, self.height))
                
        except Exception as e:
            print(f"Warning: Could not load Boss image. Using square. {e}")

        # 2. SETUP POSITION
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.y = target_y # Start near top (target position)
        self.screen_width = screen_width

        # 3. MOVEMENT & STATS
        # Default movement
        self.speed_x = 3
        # Variant tweaks (stronger boss)
        if self.variant in ("sotrak_rewop", "stark_rewop", "demon_boss"):
            self.speed_x = 5
        self.max_hp = 500
        self.hp = self.max_hp
        # Track which HP thresholds have already spawned powerups (avoid duplicates)
        self.powerup_thresholds_spawned = set()
        
        # 4. SHOOTING SETUP
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()
        # Base shoot delay (ms)
        self.shoot_delay = 1000
        if self.variant in ("sotrak_rewop", "stark_rewop", "demon_boss"):
            self.shoot_delay = 800  # slightly faster for stronger variants (nerfed)
        # Mark hard behavior for easy checks
        self.hard_behavior = self.variant in ("sotrak_rewop", "stark_rewop", "demon_boss")

    def update(self):
        # MOVE: Bounce left and right
        self.rect.x += self.speed_x
        
        # Bounce off walls
        if self.rect.right >= self.screen_width:
            self.speed_x = -abs(self.speed_x) # Go Left
        elif self.rect.left <= 0:
            self.speed_x = abs(self.speed_x)  # Go Right

        # Hard variants occasionally flip direction to be less predictable (rarer)
        if getattr(self, 'hard_behavior', False) and random.random() < 0.01:
            self.speed_x = -self.speed_x

        # SHOOT: Check timer
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = now

    def shoot(self):
        # Variant: triple spread shot for the harder boss
        if self.variant in ("sotrak_rewop", "stark_rewop", "demon_boss"):
            # Triple spread for harder variants (nerfed: no flank bullets, slightly milder velocities)
            center = BossBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=7)
            left = BossBullet(self.rect.centerx - 12, self.rect.bottom, dx=-2, dy=6)
            right = BossBullet(self.rect.centerx + 12, self.rect.bottom, dx=2, dy=6)
            self.bullets.add(center, left, right)
        else:
            # Non-variant boss: usually single straight bullet, but occasionally fire a triple spread
            if random.random() < 0.20:  # 20% chance to fire a spread shot
                center = BossBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=6)
                left = BossBullet(self.rect.centerx - 10, self.rect.bottom, dx=-1.5, dy=6)
                right = BossBullet(self.rect.centerx + 10, self.rect.bottom, dx=1.5, dy=6)
                self.bullets.add(center, left, right)
            else:
                bullet = BossBullet(self.rect.centerx, self.rect.bottom)
                self.bullets.add(bullet)