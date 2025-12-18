import pygame
import sys
import os
from objectives import sound 
import math

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 60)
BUTTON_BG = (20, 20, 30)


def draw_text_centered(screen, text, font, color, y_offset):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(screen.get_width() // 2, y_offset))
    screen.blit(img, rect)


def draw_button(screen, rect, text, font, is_hover=False):
    # Button background
    color = (YELLOW if is_hover else NEON_BLUE)
    # Outer shadow
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    shadow.fill((0,0,0,120))
    screen.blit(shadow, (rect.x + 4, rect.y + 6))

    pygame.draw.rect(screen, BUTTON_BG, rect, border_radius=8)
    pygame.draw.rect(screen, color, rect, 3, border_radius=8)

    txt = font.render(text, True, WHITE if is_hover else GRAY)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)


def draw_slider(screen, x, y, width, height, value):
    # Background bar
    pygame.draw.rect(screen, DARK_GRAY, (x, y, width, height), border_radius=6)
    # Filled portion
    filled_w = int(value * width)
    pygame.draw.rect(screen, NEON_BLUE, (x, y, filled_w, height), border_radius=6)
    # Handle
    handle_x = x + filled_w
    pygame.draw.circle(screen, WHITE, (handle_x, y + height // 2), height // 2 + 2)
    pygame.draw.circle(screen, NEON_BLUE, (handle_x, y + height // 2), height // 2)


def start_menu(screen, clock):
    # Fonts
    title_font = pygame.font.SysFont("Impact", 70)
    option_font = pygame.font.SysFont("Arial", 36)
    small_font = pygame.font.SysFont("Arial", 20)

    # 1. LOAD BACKGROUND
    bg_image = None
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "images", "menu_bg.png") 
        if os.path.exists(img_path):
            loaded_img = pygame.image.load(img_path).convert()
            bg_image = pygame.transform.scale(loaded_img, screen.get_size())
    except Exception as e:
        print(f"Error loading menu background: {e}")

    # Menu State
    menu_options = ["START GAME", "SETTINGS", "QUIT"]
    selected_index = 0
    in_settings = False
    slider_dragging = False

    # Button rects
    btn_w, btn_h = 320, 56
    btn_x = screen.get_width() // 2 - btn_w // 2
    btn_y_start = 270

    # small state to play navigation sound only when selection changes
    last_hover = None

    while True:
        # Input state
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # 2. DRAW BACKGROUND
        if bg_image:
            screen.blit(bg_image, (0, 0)) 
            # Dark overlay for readability
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(120) 
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0,0))
        else:
            screen.fill(BLACK)

        # Animated Title (subtle float)
        t = pygame.time.get_ticks() / 1000.0
        float_offset = math.sin(t * 2.0) * 6
        title_surf = title_font.render("SECTOR 48", True, NEON_BLUE)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 120 + float_offset))
        screen.blit(title_surf, title_rect)

        # 4. DRAW OPTIONS OR SETTINGS
        if not in_settings:
            for i, option in enumerate(menu_options):
                rect = pygame.Rect(btn_x, btn_y_start + i * (btn_h + 16), btn_w, btn_h)
                hover = rect.collidepoint(mouse_pos)
                # if keyboard selection is active, show hover on selected_index
                if selected_index == i:
                    hover = hover or (last_hover is None and True)
                draw_button(screen, rect, option, option_font, is_hover=hover)

                # play navigation sound when hover changes
                if hover and last_hover != i:
                    try:
                        sound.play_shoot()
                    except Exception:
                        pass
                    last_hover = i

            # Instructions
            draw_text_centered(screen, "Use ARROWS / ENTER or click a button", small_font, (200,200,200), 520)

            # Handle clicks
            if mouse_pressed[0]:
                for i in range(len(menu_options)):
                    rect = pygame.Rect(btn_x, btn_y_start + i * (btn_h + 16), btn_w, btn_h)
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            try: sound.play_explosion()
                            except Exception: pass
                            return "start"
                        elif i == 1:
                            in_settings = True
                        elif i == 2:
                            pygame.quit(); sys.exit()

        else:
            # SETTINGS: volume slider + back
            draw_text_centered(screen, "-- SETTINGS --", option_font, NEON_BLUE, 220)
            vol = sound.current_volume

            # Slider area
            slider_w, slider_h = 420, 18
            slider_x = screen.get_width() // 2 - slider_w // 2
            slider_y = 320
            draw_slider(screen, slider_x, slider_y, slider_w, slider_h, vol)

            # Percent label
            vol_percent = int(vol * 100)
            draw_text_centered(screen, f"Music Volume: {vol_percent}%", option_font, WHITE, 360)
            draw_text_centered(screen, "Click or drag the slider, or use LEFT/RIGHT", small_font, GRAY, 410)
            draw_text_centered(screen, "Press ESC or BACK to return", small_font, YELLOW, 460)

            # Slider interaction (mouse)
            if mouse_pressed[0]:
                mx, my = mouse_pos
                if mx >= slider_x and mx <= slider_x + slider_w and abs(my - (slider_y + slider_h//2)) <= 30:
                    slider_dragging = True
            else:
                slider_dragging = False

            if slider_dragging:
                mx = mouse_pos[0]
                rel = (mx - slider_x) / slider_w
                rel = max(0.0, min(1.0, rel))
                sound.set_music_volume(rel)

            # Keyboard control for volume
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                sound.set_music_volume(max(0.0, sound.current_volume - 0.01))
            if keys[pygame.K_RIGHT]:
                sound.set_music_volume(min(1.0, sound.current_volume + 0.01))

            # Back button
            back_rect = pygame.Rect(btn_x, 500, 180, 44)
            if back_rect.collidepoint(mouse_pos):
                draw_button(screen, back_rect, "BACK", option_font, is_hover=True)
                if mouse_pressed[0]:
                    in_settings = False
            else:
                draw_button(screen, back_rect, "BACK", option_font, is_hover=False)

            # Allow ESC or Enter to go back
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        in_settings = False

        # Keyboard navigation and events (outside settings to avoid interfering with slider loop above)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if not in_settings:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(menu_options)
                        try: sound.play_shoot()
                        except Exception: pass
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(menu_options)
                        try: sound.play_shoot()
                        except Exception: pass
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0: return "start"
                        elif selected_index == 1: in_settings = True
                        elif selected_index == 2: pygame.quit(); sys.exit()
                else:
                    # settings key handling for volume adjustments done above
                    pass

        pygame.display.flip()
        clock.tick(60)