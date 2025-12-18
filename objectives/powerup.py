import pygame
import random
import math

# --- POWER-UP TYPES ---
EXTRA_LIFE = "life"    # Adds +1 Life
RAPID_FIRE = "rapid"   # Shoots faster
SHIELD = "shield"      # Invincible for a few seconds

# --- COLORS ---
POWERUP_COLORS = {
    EXTRA_LIFE: (0, 255, 0),       # Green
    RAPID_FIRE: (0, 200, 255),     # Cyan
    SHIELD: (255, 255, 0),         # Yellow
}

class PowerUp:
    def __init__(self, x, y, type):
        # Increase size slightly for nicer visuals
        size = 36
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
        self.type = type
        self.speed = 3
        # Animation phase offset for variety
        self.phase = random.uniform(0, 1000)

        # Spawn animation
        self.spawn_start = pygame.time.get_ticks()
        self.spawn_duration = 300

        # Pickup animation
        self.picked = False
        self.pickup_start = None
        self.pickup_duration = 220
        self.done = False

    def start_pickup(self):
        if not self.picked:
            self.picked = True
            self.pickup_start = pygame.time.get_ticks()

    def update(self):
       
        # If pickup animation is playing, don't move
        if not self.picked:
            self.rect.y += self.speed
        else:
            # Check end of pickup
            now = pygame.time.get_ticks()
            if now - self.pickup_start >= self.pickup_duration:
                self.done = True

    def draw(self, surface):
        """Draws the power-up with spawn/pickup animations."""
        color = POWERUP_COLORS[self.type]
        cx = self.rect.centerx
        cy = self.rect.centery
        w, h = self.rect.width, self.rect.height

        now = pygame.time.get_ticks()

        # Spawn pulse (brief burst)
        spawn_progress = min(1.0, (now - self.spawn_start) / self.spawn_duration)
        if spawn_progress < 1.0:
            sp_alpha = int(180 * (1.0 - spawn_progress))
            sp_radius = int(max(w, h) * (0.8 + 0.8 * spawn_progress))
            sp_surf = pygame.Surface((sp_radius*2, sp_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(sp_surf, (*color, sp_alpha), (sp_radius, sp_radius), sp_radius)
            surface.blit(sp_surf, (cx - sp_radius, cy - sp_radius), special_flags=pygame.BLEND_PREMULTIPLIED)

        # Pick-up animation: scale up and fade out
        scale = 1.0
        alpha = 255
        if self.picked:
            prog = min(1.0, (now - self.pickup_start) / self.pickup_duration)
            scale = 1.0 + 0.6 * prog
            alpha = int(255 * (1.0 - prog))

        # Glow surface
        glow_surf = pygame.Surface((int(w*2*scale), int(h*2*scale)), pygame.SRCALPHA)
        glow_col = (*color, 110)
        glow_radius = int(max(w, h) * 0.7 * scale)
        pygame.draw.circle(glow_surf, glow_col, (glow_surf.get_width()//2, glow_surf.get_height()//2), glow_radius)
        surface.blit(glow_surf, (cx - glow_surf.get_width()//2, cy - glow_surf.get_height()//2), special_flags=pygame.BLEND_PREMULTIPLIED)

        # Base rect (drawn onto a temp surface so we can scale and apply alpha)
        base_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(base_surf, (20,20,20), (0,0,w,h), border_radius=8)
        pygame.draw.rect(base_surf, color, (3,3,w-6,h-6), border_radius=6)

        # Icon for each type
        if self.type == EXTRA_LIFE:
            # Heart icon (two circles + triangle)
            pygame.draw.circle(base_surf, (255, 60, 100), (w//2 - 6, h//2 - 4), 6)
            pygame.draw.circle(base_surf, (255, 60, 100), (w//2 + 6, h//2 - 4), 6)
            points = [(w//2 - 12, h//2 - 2), (w//2 + 12, h//2 - 2), (w//2, h//2 + 10)]
            pygame.draw.polygon(base_surf, (255, 60, 100), points)
        elif self.type == RAPID_FIRE:
            # Speed lines / bullets
            for i in range(3):
                offset = -10 + i * 10
                r = pygame.Rect(w//2 + offset, h//2 - 2 - i*2, 12, 6)
                pygame.draw.rect(base_surf, (255, 240, 100), r, border_radius=3)
                trail = pygame.Rect(w//2 + offset - 8, h//2 - 1 - i*2, 6, 2)
                pygame.draw.rect(base_surf, (255, 220, 60), trail, border_radius=2)
        elif self.type == SHIELD:
            # Concentric rings for shield
            pygame.draw.circle(base_surf, (255,255,255), (w//2, h//2), 8, 2)
            pygame.draw.circle(base_surf, (120, 200, 255), (w//2, h//2), 12, 2)
            pygame.draw.arc(base_surf, (200, 255, 255), (w//2 - 16, h//2 - 16, 32, 32), 0.2, 1.2, 3)

        pygame.draw.rect(base_surf, (255,255,255), (0,0,w,h), 2, border_radius=8)

        # Scale & alpha
        if scale != 1.0:
            scaled = pygame.transform.smoothscale(base_surf, (int(w*scale), int(h*scale)))
        else:
            scaled = base_surf
        if alpha < 255:
            scaled.set_alpha(alpha)

        surface.blit(scaled, (cx - scaled.get_width()//2, cy - scaled.get_height()//2))

# --- SPAWN FUNCTION ---
def spawn_powerup_at(powerups_list, x, y):
    """
    Called when an enemy dies. 
    Has a 15% chance to drop a random power-up.
    """
    if random.random() < 0.15:  # 15% chance
        # Pick a random type
        power_type = random.choice([EXTRA_LIFE, RAPID_FIRE, SHIELD])
        
        # Create object
        new_powerup = PowerUp(x, y, power_type)
        
        # Add to the main list
        powerups_list.append(new_powerup)