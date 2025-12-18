import pygame
import sys
import os
from objectives import sound

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0) # Color for High Score

def game_over_screen(screen, clock, current_score, best_score):
    font = pygame.font.SysFont("Arial", 36)
    title_font = pygame.font.SysFont("Arial", 60)
    score_font = pygame.font.SysFont("Arial", 50) # Font for numbers

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
            screen.blit(overlay, (0,0))
        else:
            screen.fill(BLACK) 

        # 3. DRAW TITLE
        title_text = title_font.render("GAME OVER", True, WHITE)
        screen.blit(title_text, (screen.get_width()//2 - title_text.get_width()//2, 100))

        # 4. DRAW SCORES (New!)
        score_surf = score_font.render(f"SCORE: {current_score}", True, WHITE)
        best_surf = score_font.render(f"BEST: {best_score}", True, GOLD)

        screen.blit(score_surf, (screen.get_width()//2 - score_surf.get_width()//2, 200))
        screen.blit(best_surf, (screen.get_width()//2 - best_surf.get_width()//2, 260))

        # 5. DRAW INSTRUCTIONS
        info_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(info_text, (screen.get_width()//2 - info_text.get_width()//2, 450))

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