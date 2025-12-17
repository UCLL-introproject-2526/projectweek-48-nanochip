import pygame
import sys
import os
from objectives import sound 

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

def draw_text_centered(screen, text, font, color, y_offset):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(screen.get_width() // 2, y_offset))
    screen.blit(img, rect)

def start_menu(screen, clock):
    # Fonts
    title_font = pygame.font.SysFont("Impact", 70)
    option_font = pygame.font.SysFont("Arial", 40)
    small_font = pygame.font.SysFont("Arial", 24)

    # ----------------------------------------------------
    # 1. LOAD BACKGROUND IMAGE
    # ----------------------------------------------------
    bg_image = None
    try:
        # Get path to objectives/images/
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # CHANGE "menu_bg.jpg" TO YOUR FILENAME (e.g. "spaceship.jpg")
        img_path = os.path.join(base_dir, "images", "menu_bg.png") 
        
        if os.path.exists(img_path):
            loaded_img = pygame.image.load(img_path).convert()
            # Scale it to fit the screen window
            bg_image = pygame.transform.scale(loaded_img, screen.get_size())
        else:
            print(f"Menu background not found at: {img_path}")
    except Exception as e:
        print(f"Error loading menu background: {e}")

    # Menu State
    menu_options = ["START GAME", "SETTINGS", "QUIT"]
    selected_index = 0
    in_settings = False 

    while True:
        # ----------------------------------------------------
        # 2. DRAW BACKGROUND
        # ----------------------------------------------------
        if bg_image:
            screen.blit(bg_image, (0, 0)) # Draw image
            # Optional: Draw a semi-transparent black overlay so text is readable
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(150) # 0 is transparent, 255 is solid
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0,0))
        else:
            screen.fill(BLACK) # Fallback if no image

        # # ----------------------
        # # DRAW TITLE
        # # ----------------------
        # draw_text_centered(screen, "SECTOR 48", small_font, NEON_BLUE, 100)
        # draw_text_centered(screen, "NANOCHIP", title_font, WHITE, 150)

        # ----------------------
        # DRAW MENU OPTIONS
        # ----------------------
        if not in_settings:
            for i, option in enumerate(menu_options):
                if i == selected_index:
                    color = YELLOW
                    prefix = "> "
                else:
                    color = GRAY
                    prefix = "  "
                draw_text_centered(screen, prefix + option, option_font, color, 300 + (i * 60))
            
            draw_text_centered(screen, "Use ARROW KEYS and ENTER", small_font, (200, 200, 200), 550)

        else:
            # Settings Menu
            draw_text_centered(screen, "-- SETTINGS --", option_font, NEON_BLUE, 250)
            vol_percent = int(sound.current_volume * 100)
            draw_text_centered(screen, f"Music Volume: < {vol_percent}% >", option_font, WHITE, 350)
            draw_text_centered(screen, "Use LEFT/RIGHT to change volume", small_font, GRAY, 420)
            draw_text_centered(screen, "Press ESC or ENTER to go back", small_font, YELLOW, 500)

        pygame.display.flip()

        # ----------------------
        # INPUT HANDLING
        # ----------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not in_settings:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0: return "start"
                        elif selected_index == 1: in_settings = True
                        elif selected_index == 2:
                            pygame.quit()
                            sys.exit()
                else:
                    if event.key == pygame.K_LEFT:
                        sound.set_music_volume(sound.current_volume - 0.1)
                    elif event.key == pygame.K_RIGHT:
                        sound.set_music_volume(sound.current_volume + 0.1)
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        in_settings = False

        clock.tick(60)