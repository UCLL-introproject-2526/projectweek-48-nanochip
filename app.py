import pygame
import sys
import random
import os

# --------------------
# INIT
# --------------------
pygame.init()
pygame.mixer.init()

# --------------------
# IMPORT MODULES
# --------------------
from objectives import sound
from objectives.background import Background
from objectives import health
import objectives.Smarter_enemies as smarter_enemies
from objectives.game_over import game_over_screen
from objectives import start_menu
from objectives.explosion import Explosion

# --------------------
# SOUND INIT
# --------------------
sound.init_sound()
sound.play_background_music()

# --------------------
# DISPLAY
# --------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()

# --------------------
# COLORS & FONT
# --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
font = pygame.font.SysFont(None, 36)

# --------------------
# PLAYER
# --------------------
player_width, player_height = 50, 40
player_speed = 6
player_max_hp = 100
damage_per_hit = 20
invincible_duration = 1000

# --------------------
# ENEMIES
# --------------------
enemy_width, enemy_height = 50, 40
enemy_speed = 3

# --------------------
# BULLETS & ENEMIES
# --------------------
bullets = []
enemies = []
spawn_timer = 0

# --------------------
# GAME STATE
# --------------------
GAME_RUNNING = "running"
GAME_OVER = "over"
game_state = GAME_RUNNING

# --------------------
# BACKGROUND
# --------------------
bg = Background("spaceship.jpg", WIDTH, HEIGHT)

# --------------------
# LOAD IMAGES
# --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

player_img_path = os.path.join(BASE_DIR, "objectives", "images", "player_ship.png")
enemy_img_path = os.path.join(BASE_DIR, "objectives", "images", "enemy_ship.png")

player_img = pygame.image.load(player_img_path).convert_alpha()
player_img = pygame.transform.scale(player_img, (player_width, player_height))

enemy_img = pygame.image.load(enemy_img_path).convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))

# --------------------
# EXPLOSIONS
# --------------------
explosions = []

# --------------------
# INITIALIZE VARIABLES
# --------------------
player_x = 0
player_y = 0
player_hp = 0
player_lives = 0
score = 0
last_hit_time = 0

# --------------------
# RESET GAME FUNCTION
# --------------------
def reset_game():
    global player_x, player_y, player_hp, player_lives
    global bullets, enemies, score, spawn_timer, last_hit_time, game_state, explosions

    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 70
    player_hp = player_max_hp
    player_lives = 3

    bullets.clear()
    enemies.clear()
    explosions.clear()
    score = 0
    spawn_timer = 0
    last_hit_time = 0

    sound.play_background_music()
    game_state = GAME_RUNNING

# --------------------
# DRAW PLAYER
# --------------------
def draw_player(x, y):
    screen.blit(player_img, (x, y))

# --------------------
# START MENU
# --------------------
action = start_menu.start_menu(screen, clock)
if action is None:
    action = "start"
reset_game()

# --------------------
# MAIN GAME LOOP
# --------------------
running = True
while running:
    clock.tick(60)

    # --------------------
    # EVENTS
    # --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == GAME_RUNNING and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(
                    pygame.Rect(
                        player_x + player_width // 2 - 3,
                        player_y,
                        6,
                        12,
                    )
                )
                sound.play_shoot()

    # --------------------
    # GAME OVER STATE
    # --------------------
    if game_state == GAME_OVER:
        action = game_over_screen(screen, clock)
        if action == "restart":
            reset_game()
        continue

    # --------------------
    # PLAYER INPUT (WRAP-AROUND)
    # --------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        if player_x + player_width < 0:
            player_x = WIDTH
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        if player_x > WIDTH:
            player_x = -player_width

    # --------------------
    # DRAW BACKGROUND
    # --------------------
    bg.draw(screen)

    # --------------------
    # BULLETS
    # --------------------
    for bullet in bullets[:]:
        bullet.y -= 8
        if bullet.y < 0:
            bullets.remove(bullet)

    # --------------------
    # ENEMY SPAWN
    # --------------------
    spawn_timer += 1
    if spawn_timer > 40:
        smarter_enemies.spawn_enemy(enemies, WIDTH, enemy_width, enemy_height)
        spawn_timer = 0

    # --------------------
    # ENEMY UPDATE (3 CHASE PLAYER)
    # --------------------
    score = smarter_enemies.update_enemies(
        enemies=enemies,
        bullets=bullets,
        enemy_speed=enemy_speed,
        score=score,
        sound=sound,
        screen_height=HEIGHT,
        explosions=explosions,
        player_x=player_x,
        player_y=player_y
    )

    # --------------------
    # COLLISION WITH PLAYER
    # --------------------
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    current_time = pygame.time.get_ticks()

    for enemy in enemies[:]:
        if player_rect.colliderect(enemy):
            if current_time - last_hit_time > invincible_duration:
                player_hp -= damage_per_hit
                last_hit_time = current_time
                explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                enemies.remove(enemy)
                sound.play_explosion()

    # --------------------
    # GAME OVER CHECK
    # --------------------
    if player_hp <= 0:
        player_lives -= 1
        if player_lives > 0:
            player_hp = player_max_hp
            enemies.clear()
            bullets.clear()
            explosions.clear()
            pygame.time.delay(800)
        else:
            sound.stop_background_music()
            sound.play_game_over()
            game_state = GAME_OVER

    # --------------------
    # DRAW PLAYER (FLASH)
    # --------------------
    if current_time - last_hit_time < invincible_duration:
        if (current_time // 100) % 2 == 0:
            draw_player(player_x, player_y)
    else:
        draw_player(player_x, player_y)

    # --------------------
    # DRAW BULLETS & ENEMIES
    # --------------------
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))

    # --------------------
    # DRAW EXPLOSIONS
    # --------------------
    for exp in explosions[:]:
        exp.update()
        exp.draw(screen)
        if exp.is_dead():
            explosions.remove(exp)

    # --------------------
    # UI
    # --------------------
    health.draw_health_bar(screen, 10, 10, player_hp, player_max_hp)
    health.draw_lives(screen, 10, 40, player_lives, font)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.flip()

pygame.quit()
