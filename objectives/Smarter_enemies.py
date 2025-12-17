import pygame
import random
from objectives.explosion import Explosion

def spawn_enemy(enemies, screen_width, enemy_width=50, enemy_height=40):
    """
    Spawns an enemy fully inside the screen using the image dimensions
    """
    x = random.randint(0, screen_width - enemy_width)
    y = -enemy_height
    enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))


def update_enemies(
    enemies,
    bullets,
    enemy_speed,
    score,
    sound,
    screen_height,
    explosions=None,
    player_x=None,
    player_y=None
):
    """
    Handles enemy movement:
    - Only 3 enemies actively chase the player
    - Others move straight down
    - Handles bullet collisions and dodging
    """
    if len(enemies) > 0:
        chasing_enemies = random.sample(enemies, min(3, len(enemies)))
    else:
        chasing_enemies = []

    for enemy in enemies[:]:
        # Chasing behavior
        if enemy in chasing_enemies and player_x is not None and player_y is not None:
            dx = player_x + 25 - (enemy.x + enemy.width // 2)
            dy = player_y + 20 - (enemy.y + enemy.height // 2)
            distance = max((dx**2 + dy**2)**0.5, 1)
            enemy.x += int(enemy_speed * dx / distance)
            enemy.y += int(enemy_speed * dy / distance)
        else:
            enemy.y += enemy_speed  # straight down

        # Remove off-screen enemies
        if enemy.y > screen_height:
            enemies.remove(enemy)
            continue

        # Bullet dodging
        dodges = 1
        for bullet in bullets[:]:
            bullet_is_threatening = (
                abs(bullet.centerx - enemy.centerx) < enemy.width
                and bullet.y < enemy.y
            )
            if bullet_is_threatening and dodges > 0:
                dodge = random.choice([enemy.x - 15, enemy.x + 15])
                enemy.x = dodge
                dodges -= 1

            # Collision with bullet
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                sound.play_explosion()
                if explosions is not None:
                    explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                score += 1
                break

    return score




# import pygame
# import random
# from random import choices
# # --------------------
# # INIT
# # --------------------
# pygame.init()
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Spaceship Game")
# clock = pygame.time.Clock()

# # --------------------
# # COLORS
# # --------------------
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)

# # --------------------
# # PLAYER
# # --------------------
# player_width, player_height = 50, 40
# player_x = WIDTH // 2 - player_width // 2
# player_y = HEIGHT - 70
# player_speed = 6

# # --------------------
# # BULLETS
# # --------------------
# bullets = []
# bullet_speed = 8

# # --------------------
# # ENEMIES
# # --------------------
# enemies = []
# enemy_speed = 3
# spawn_timer = 0

# # --------------------
# # SCORE
# # --------------------
# score = 0
# font = pygame.font.SysFont(None, 36)

# def draw_player(x, y):
#     pygame.draw.polygon(
#         screen,
#         WHITE,
#         [(x, y + player_height), (x + player_width // 2, y), (x + player_width, y + player_height)]
#     )

# def draw_score():
#     text = font.render(f"Score: {score}", True, WHITE)
#     screen.blit(text, (10, 10))

# # --------------------
# # GAME LOOP
# # --------------------
# running = True
# while running:
#     clock.tick(60)
#     screen.fill(BLACK)

#     # EVENTS
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 bullets.append(pygame.Rect(player_x + player_width // 2 - 3, player_y, 6, 12))
#         # if event.type == randomize_dodging:
#         #     randomize_dodging()
#     # INPUT
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT] and player_x > 0:
#         player_x -= player_speed
#     if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
#         player_x += player_speed

#     # BULLETS UPDATE
#     for bullet in bullets[:]:
#         bullet.y -= bullet_speed
#         if bullet.y < 0:
#             bullets.remove(bullet)

#     # ENEMY SPAWN
#     spawn_timer += 1
#     if spawn_timer > 40:
#         enemies.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 30))
#         spawn_timer = 0
#     #  if score > 3:
#     #     spawn_timer = 20
#     #     enemies.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 30))
#     #     spawn_timer = 0 
#    # ENEMY UPDATE
#     for enemy in enemies[:]:
#         dodges = 1
#         enemy.y += enemy_speed
#         if enemy.y > HEIGHT:
#             enemies.remove(enemy)

#         # COLLISION WITH BULLETS
#         for bullet in bullets[:]:
#         #   def randomize_dodging():
#         #     randomize_dodging = pygame.USEREVENT + 0
#         #     pygame.time.set_timer(randomize_dodging, 5000)
#             bullet_is_threatening = False
#             dodge_to_right = enemy.x + 10
#             dodge_to_left = enemy.x - 10
#             danger_width = enemy.width
#             if abs(bullet.x - enemy.x) < danger_width:

#                 # bullet_is_threatening = True
#             # if abs(bullet.centerx-enemy.centerx)< danger_width and bullet.y < enemy.y:
#                 bullet_is_threatening = True 
#             if bullet_is_threatening ==True:
#                 if dodges > 0:
#                     choice = choices ([dodge_to_right, dodge_to_left], [0.5, 0.5])[0] 
#                     enemy.x = choice 
#                 dodges = dodges - 1
#             # randomize_dodging()
#             if enemy.colliderect(bullet):
#                 enemies.remove(enemy)
#                 bullets.remove(bullet)
#                 score += 1
#                 break

#     # DRAW
#     draw_player(player_x, player_y)
#     for bullet in bullets:
#         pygame.draw.rect(screen, WHITE, bullet)
#     for enemy in enemies:
#         pygame.draw.rect(screen, RED, enemy)

#     draw_score()
#     pygame.display.flip()

# pygame.quit()