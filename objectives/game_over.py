import pygame
import sys
import os
from objectives import sound

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0) # Color for High Score


# helper to draw outlined text (2D look) - module level reuse
def draw_outlined_text(target, text, font_obj, pos, fg_color, outline_color=(0,0,0), outline_width=3):
    base = font_obj.render(text, True, fg_color)
    ox, oy = pos
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx == 0 and dy == 0:
                continue
            target.blit(font_obj.render(text, True, outline_color), (ox+dx, oy+dy))
    # slight drop shadow
    try:
        target.blit(font_obj.render(text, True, (0,0,0)), (ox+2, oy+2))
    except Exception:
        pass
    target.blit(base, (ox, oy))


def game_over_screen(screen, clock, current_score, best_score):
    font = pygame.font.SysFont("Arial", 36)
    title_font = pygame.font.SysFont("Arial", 60)
    score_font = pygame.font.SysFont("Arial", 50)  # Font for numbers

    # 1. LOAD BACKGROUND IMAGE
    bg_image = None
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "images", "game_over.jpg")

        if os.path.exists(img_path):
            loaded_img = pygame.image.load(img_path).convert()
            bg_image = pygame.transform.scale(loaded_img, screen.get_size())
    except Exception as e:
        print(f"Error loading game over image: {e}")

    sound.play_game_over()

    while True:
        # 2. DRAW BACKGROUND
        if bg_image:
            screen.blit(bg_image, (0, 0))
            # Dark overlay
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill(BLACK)

        # 3. DRAW TITLE
        title_text = title_font.render("GAME OVER", True, WHITE)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))

        # 4. DRAW SCORES (New!) using outlined text for better contrast
        score_text = f"SCORE: {current_score}"
        best_text = f"BEST: {best_score}"
        draw_outlined_text(screen, score_text, score_font, (screen.get_width() // 2 - score_font.size(score_text)[0] // 2, 200), WHITE, outline_color=(10,10,10), outline_width=2)
        draw_outlined_text(screen, best_text, score_font, (screen.get_width() // 2 - score_font.size(best_text)[0] // 2, 260), GOLD, outline_color=(10,10,10), outline_width=2)

        # 5. DRAW INSTRUCTIONS
        info_str = "Press R to Restart or Q to Quit"
        draw_outlined_text(screen, info_str, font, (screen.get_width() // 2 - font.size(info_str)[0] // 2, 450), WHITE, outline_color=(10,10,10), outline_width=2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(60)


def victory_screen(screen, clock, current_score, best_score):
    font = pygame.font.SysFont("Arial", 36)
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    msg_font = pygame.font.SysFont("Arial", 56, bold=True)

    # Load victory background if available
    bg_image = None
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "images", "victory_bg.jpg")
        if os.path.exists(img_path):
            loaded = pygame.image.load(img_path).convert()
            bg_image = pygame.transform.scale(loaded, screen.get_size())
    except Exception as e:
        print(f"Error loading victory image: {e}")

    # Stop other music and optionally play victory sound if available
    try:
        sound.stop_background_music()
    except Exception:
        pass
    try:
        sound.play_victory()
    except Exception:
        pass

    message = "You Cleared the Sector 48 : NanoChip. You Won."
    # split into two lines for better centering and spacing
    lines = ["You Cleared the Sector 48", "NanoChip. You Won."]

    while True:
        # draw background
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Prepare metrics
        max_w = 0
        total_h = 0
        spacing = 12
        colors = [GOLD, WHITE]
        fonts = [title_font, msg_font]
        rendered = []
        for i, line in enumerate(lines):
            f = fonts[i]
            surf = f.render(line, True, colors[i])
            rendered.append((line, f, colors[i], surf))
            max_w = max(max_w, surf.get_width())
            total_h += surf.get_height()
            if i < len(lines) - 1:
                total_h += spacing

        # Backdrop for readability
        pad_x = 36
        pad_y = 26
        block_w = max_w + pad_x * 2
        block_h = total_h + pad_y * 2
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        block_rect = pygame.Rect(center_x - block_w // 2, center_y - block_h // 2, block_w, block_h)
        backdrop = pygame.Surface((block_rect.w, block_rect.h), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 180))
        screen.blit(backdrop, (block_rect.x, block_rect.y))

        # helper to draw outlined text (2D look)
        def draw_outlined_text(target, text, font_obj, pos, fg_color, outline_color=(0,0,0), outline_width=3):
            # render main and outline
            base = font_obj.render(text, True, fg_color)
            ox, oy = pos
            # draw outline by rendering text in outline_color with offsets
            for dx in range(-outline_width, outline_width+1):
                for dy in range(-outline_width, outline_width+1):
                    if dx == 0 and dy == 0:
                        continue
                    target.blit(font_obj.render(text, True, outline_color), (ox+dx, oy+dy))
            # small drop shadow for depth
            target.blit(font_obj.render(text, True, (0,0,0,)), (ox+2, oy+2))
            # main text
            target.blit(base, (ox, oy))

        # Render lines centered within the block with outlines
        y = block_rect.y + pad_y
        for i, (line, fobj, clr, surf) in enumerate(rendered):
            x = center_x - surf.get_width() // 2
            out_w = 4 if i == 0 else 3
            draw_outlined_text(screen, line, fobj, (x, y), clr, outline_color=(10,10,10), outline_width=out_w)
            y += surf.get_height() + spacing

        # Draw score and instruction below the block using outlined text
        score_text = f"SCORE: {current_score}"
        draw_outlined_text(screen, score_text, font, (center_x - font.size(score_text)[0]//2, block_rect.y + block_rect.h + 16), WHITE, outline_color=(10,10,10), outline_width=2)

        info_str = "Press R to Restart or Q to Quit"
        draw_outlined_text(screen, info_str, font, (center_x - font.size(info_str)[0]//2, screen.get_height() - 100), WHITE, outline_color=(10,10,10), outline_width=2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(60)