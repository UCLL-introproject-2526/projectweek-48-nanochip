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

        # Variant sizing:
        if self.variant in ("sotrak_rewop", "stark_rewop"):
            # Very large for these hard variants
            self.width = int(self.width * 2)
            self.height = int(self.height * 2)
        elif self.variant == "demon_boss":
            # Make demon visually larger
            self.width = int(self.width * 1.6)
            self.height = int(self.height * 1.6)
        elif self.variant == "final_boss":
            # Final boss is very large
            self.width = int(self.width * 2.2)
            self.height = int(self.height * 2.2)

        # Default image surface (fallback)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((150, 0, 0)) # Dark Red
        
        # Try to load a variant-specific image if it exists, otherwise keep the fallback
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            variant_name = self.variant or "alien_boss"
            img_path = os.path.join(base_dir, "images", f"{variant_name}.png")
            if os.path.exists(img_path):
                loaded_img = pygame.image.load(img_path).convert_alpha()
                self.image = pygame.transform.scale(loaded_img, (self.width, self.height))
            else:
                # If no image file exists, apply a variant-specific decoration so the boss is distinguishable
                if self.variant == "final_boss":
                    # Draw a simple 'final' look: eyes and horns
                    pygame.draw.rect(self.image, (40, 0, 0), (0, 0, self.width, self.height))
                    # Horns
                    pygame.draw.polygon(self.image, (80, 10, 10), [(5,5), (self.width*0.2, 5), (self.width*0.07, self.height*0.25)])
                    pygame.draw.polygon(self.image, (80, 10, 10), [(self.width-5,5), (self.width*0.8, 5), (self.width*0.93, self.height*0.25)])
                    # Eyes
                    pygame.draw.circle(self.image, (255, 40, 40), (int(self.width*0.35), int(self.height*0.35)), int(self.width*0.08))
                    pygame.draw.circle(self.image, (255, 40, 40), (int(self.width*0.65), int(self.height*0.35)), int(self.width*0.08))
                    # Mouth
                    pygame.draw.rect(self.image, (20,20,20), (int(self.width*0.35), int(self.height*0.6), int(self.width*0.3), int(self.height*0.12)), border_radius=6)
                else:
                    # neutral decoration for other variants
                    pygame.draw.rect(self.image, (120, 0, 0), (2, 2, self.width-4, self.height-4), 3, border_radius=8)
        except Exception as e:
            print(f"Warning: Could not load Boss image. Using fallback draw. {e}")

        # 2. SETUP POSITION
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.y = target_y # Start near top (target position)
        self.screen_width = screen_width

        # 3. MOVEMENT & STATS
        # Default movement
        self.speed_x = 3
        # Variant tweaks (stronger boss moves faster)
        if self.variant in ("sotrak_rewop", "stark_rewop"):
            self.speed_x = 5
        elif self.variant == "demon_boss":
            # Demon is larger and more aggressive: slightly faster horizontal movement
            self.speed_x = 5
        elif self.variant == "alien_boss":
            # Make the first boss (alien) a bit less aggressive horizontally
            self.speed_x = 3
        elif self.variant == "final_boss":
            # Final boss slides across aggressively but not too fast
            self.speed_x = 4
        self.max_hp = 500
        self.hp = self.max_hp
        # Track which HP thresholds have already spawned powerups (avoid duplicates)
        self.powerup_thresholds_spawned = set()
        
        # 4. SHOOTING SETUP
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()
        # Base shoot delay (ms), spread chance, and double-burst chance
        self.shoot_delay = 1000
        self.spread_chance = 0.20
        self.double_burst_chance = 0.05
        if self.variant in ("sotrak_rewop", "stark_rewop"):
            self.shoot_delay = 800  # slightly faster for strongest variants
            self.spread_chance = 0.45
            self.double_burst_chance = 0.10
        elif self.variant == "demon_boss":
            self.shoot_delay = 700  # faster firing to make Demon more threatening
            self.spread_chance = 0.50
            self.double_burst_chance = 0.15
        elif self.variant == "alien_boss":
            # Slightly easier: slower firing and fewer spreads
            self.shoot_delay = 800
            # Alien boss shoots spreads less often and double bursts are rarer
            self.spread_chance = 0.50
            self.double_burst_chance = 0.15
        elif self.variant == "final_boss":
            # Final boss: aggressive firing but with distinct patterns tuned in shoot()
            self.shoot_delay = 500
            self.spread_chance = 0.85
            self.double_burst_chance = 0.45
        # Mark hard behavior for easy checks (Demon & Final are hard)
        self.hard_behavior = self.variant in ("sotrak_rewop", "stark_rewop", "demon_boss", "final_boss")

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
        # Hardest variants (sotrak/stark): triple spread as before
        if self.variant in ("sotrak_rewop", "stark_rewop"):
            center = BossBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=7)
            left = BossBullet(self.rect.centerx - 12, self.rect.bottom, dx=-2, dy=6)
            right = BossBullet(self.rect.centerx + 12, self.rect.bottom, dx=2, dy=6)
            self.bullets.add(center, left, right)
        elif self.variant == "demon_boss":
            # Demon: moderate spread
            center = BossBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=6)
            left = BossBullet(self.rect.centerx - 10, self.rect.bottom, dx=-1, dy=6)
            right = BossBullet(self.rect.centerx + 10, self.rect.bottom, dx=1, dy=6)
            self.bullets.add(center, left, right)
        elif self.variant == "alien_boss":
            # Alien boss: fires spread shots frequently; often wide 5-bullet bursts and sometimes double bursts
            if random.random() < self.spread_chance:
                # 25% of spread events produce a wider 5-bullet burst (narrower than before)
                if random.random() < 0.25:
                    petals = [(-20, -2), (-10, -1.2), (0, -0.2), (10, 1.2), (20, 2)]
                    for ox, dx in petals:
                        self.bullets.add(BossBullet(self.rect.centerx + ox, self.rect.bottom, dx=dx, dy=6))
                else:
                    center = BossBullet(self.rect.centerx, self.rect.bottom, dx=0, dy=7)
                    left = BossBullet(self.rect.centerx - 12, self.rect.bottom, dx=-2, dy=6)
                    right = BossBullet(self.rect.centerx + 12, self.rect.bottom, dx=2, dy=6)
                    self.bullets.add(center, left, right)

                # Chance to fire a quick second burst shifted left or right
                if random.random() < self.double_burst_chance:
                    offset = -20 if random.random() < 0.5 else 20
                    petals2 = [(-12, -1.8), (-6, -0.9), (0, -0.2), (6, 0.9), (12, 1.8)]
                    for ox, dx in petals2:
                        self.bullets.add(BossBullet(self.rect.centerx + ox + offset, self.rect.bottom, dx=dx, dy=6))
            else:
                # Straight bullet as fallback
                bullet = BossBullet(self.rect.centerx, self.rect.bottom)
                self.bullets.add(bullet)
        elif self.variant == "final_boss":
            # Final boss: very heavy, multi-pattern attacks — wide 7-bullet spread + occasional ring/double waves
            # Primary wide 7-bullet spread
            angles = [(-30, -3.5), (-18, -2.2), (-9, -1.2), (0, -0.2), (9, 1.0), (18, 2.2), (30, 3.5)]
            for ox, dx in angles:
                self.bullets.add(BossBullet(self.rect.centerx + ox, self.rect.bottom, dx=dx, dy=8))

            # 30% chance to follow with a denser ring / wave
            if random.random() < 0.30:
                for i in range(-6, 7):
                    self.bullets.add(BossBullet(self.rect.centerx + i*8, self.rect.bottom, dx=i*0.7, dy=6))

            # 40% chance to emit a close double-wide burst as well
            if random.random() < 0.40:
                offset = -16 if random.random() < 0.5 else 16
                burst = [(-12, -1.8), (-6, -0.9), (0, -0.2), (6, 0.9), (12, 1.8)]
                for ox, dx in burst:
                    self.bullets.add(BossBullet(self.rect.centerx + ox + offset, self.rect.bottom, dx=dx, dy=7))
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