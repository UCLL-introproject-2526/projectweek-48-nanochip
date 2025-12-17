import pygame
import random

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
        self.rect = pygame.Rect(x, y, 30, 30) # Slightly larger size (30x30)
        self.type = type
        self.speed = 3
        # Font to draw the letter (L, R, S)
        self.font = pygame.font.SysFont(None, 24)

    def update(self):
        """Moves the power-up down"""
        self.rect.y += self.speed

    def draw(self, surface):
        """Draws the power-up box with a letter inside"""
        color = POWERUP_COLORS[self.type]
        
        # 1. Draw the colored square
        pygame.draw.rect(surface, color, self.rect)
        
        # 2. Draw a white border (to make it pop)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        # 3. Draw the Letter (L, R, S) in black
        letter = self.type[0].upper() # Get first letter
        text = self.font.render(letter, True, (0, 0, 0))
        
        # Center the letter inside the square
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

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