# objectives/start_menu.py
import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def start_menu(screen, clock):
    font_title = pygame.font.SysFont("Arial", 60)
    font_option = pygame.font.SysFont("Arial", 36)

    while True:
        screen.fill(BLACK)

        # Title
        title_text = font_title.render("SPACESHIP GAME", True, WHITE)
        screen.blit(
            title_text,
            (screen.get_width() // 2 - title_text.get_width() // 2, 150)
        )

        # Options
        start_text = font_option.render("Press ENTER to Start", True, WHITE)
        quit_text = font_option.render("Press Q to Quit", True, WHITE)

        screen.blit(
            start_text,
            (screen.get_width() // 2 - start_text.get_width() // 2, 300)
        )
        screen.blit(
            quit_text,
            (screen.get_width() // 2 - quit_text.get_width() // 2, 350)
        )

        pygame.display.flip()

        # Event Handling
        for event in pygame.event.get():
        
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER to start
                    return "start"
                if event.key == pygame.K_q:       # Q to quit
                    pygame.quit()
                    sys.exit()

        clock.tick(60)
