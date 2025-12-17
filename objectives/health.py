import pygame

# --- SPACE THEME COLORS ---
NEON_RED = (255, 50, 80)     # Neon Red
NEON_BLUE = (0, 255, 255)    # Neon Cyan
DARK_BG = (30, 30, 50)       # Dark background for the bar
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_segmented_bar(screen, x, y, current, max_val, color, width, height, segments=10):
    """
    Function to draw a Segmented Bar (blocks).
    """
    # 1. Draw the Container Frame
    container_width = width + 10
    container_height = height + 10
    
    
    # Thin white border
    pygame.draw.rect(screen, WHITE, (x, y, container_width, container_height), 2, border_radius=5)
    
    # Semi-transparent black background inside
    surface = pygame.Surface((container_width, container_height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 100)) 
    screen.blit(surface, (x, y))

    # 2. Calculate Segment Size
    gap = 4 # Gap between segments
    
    # Actual width of one segment
    segment_width = (width - (gap * (segments - 1))) / segments
    
    # Calculate percentage
    if max_val <= 0: max_val = 1
    percent = current / max_val
    
    # Calculate active segments
    active_segments = int(percent * segments)
    
    # Visual fix: If HP > 0 but less than 1 full segment, show at least 1 segment
    if current > 0 and active_segments == 0:
        active_segments = 1

    # 3. Loop to draw each segment
    for i in range(segments):
        seg_x = x + 5 + (i * (segment_width + gap))
        seg_y = y + 5
        
        if i < active_segments:
            # Active segment (Lit up)
            pygame.draw.rect(screen, color, (seg_x, seg_y, segment_width, height), border_radius=2)
        else:
            # Empty segment (Dark)
            pygame.draw.rect(screen, DARK_BG, (seg_x, seg_y, segment_width, height), border_radius=2)

def draw_heart_icon(screen, x, y):
    """Draw Pixel Art Heart Icon"""
    color = NEON_RED
    pygame.draw.rect(screen, color, (x + 5, y, 5, 5))
    pygame.draw.rect(screen, color, (x + 20, y, 5, 5))
    pygame.draw.rect(screen, color, (x, y + 5, 30, 5))
    pygame.draw.rect(screen, color, (x + 5, y + 10, 20, 5))
    pygame.draw.rect(screen, color, (x + 10, y + 15, 10, 5))
    pygame.draw.rect(screen, color, (x + 12.5, y + 20, 5, 5))

def draw_pilot_icon(screen, x, y):
    """Draw Pilot / Player Icon"""
    color = NEON_BLUE
    # Head (Helmet)
    pygame.draw.circle(screen, color, (x + 15, y + 8), 8)
    pygame.draw.rect(screen, WHITE, (x + 12, y + 6, 6, 4))
    # Body
    pygame.draw.rect(screen, color, (x + 5, y + 18, 20, 12), border_radius=4)

# -----------------------------------------------------
# MAIN FUNCTIONS (Called by app.py)
# -----------------------------------------------------

def draw_health_bar(screen, x, y, current_hp, max_hp):
    """
    Draw Health Bar: 5 separate segments
    """
    draw_heart_icon(screen, x, y + 5)

    draw_segmented_bar(
        screen, 
        x + 40, y,          
        current_hp, max_hp, 
        NEON_RED,           
        100, 15,            
        segments=5          # Split into 5 large blocks
    )

def draw_lives(screen, x, y, lives, font=None):
    """
    Draw Lives Bar: 3 separate segments
    """
    max_lives = 3 # Max lives to display
    
    draw_pilot_icon(screen, x, y + 2)

    draw_segmented_bar(
        screen, 
        x + 40, y,          
        lives, max_lives,   
        NEON_BLUE,          
        50, 10,            
        segments=3          # Split into 3 blocks (1 per life)
    )