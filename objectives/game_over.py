# game_over.py
import pygame
import sys
from objectives import sound

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def game_over_screen(screen, clock):
    font = pygame.font.SysFont("Arial", 36)
    title_font = pygame.font.SysFont("Arial", 60)

    sound.play_game_over()

    while True:
        screen.fill(BLACK)

        title_text = title_font.render("GAME OVER", True, WHITE)
        info_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

        screen.blit(
            title_text,
            (screen.get_width() // 2 - title_text.get_width() // 2, 200)
        )
        screen.blit(
            info_text,
            (screen.get_width() // 2 - info_text.get_width() // 2, 300)
        )

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
