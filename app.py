# Simple Spaceship Game using Pygame
# Run with: python app.py

import sys
import pygame
import random
from random import choices

# --------------------
# IMPORT MODULES
# --------------------
from objectives import sound
from objectives.background import Background
from objectives import health
from objectives import Smarter_enemies


# --------------------
# INIT
# --------------------

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()

# --------------------
# BACKGROUND
# --------------------
bg = Background("spaceship.jpg", WIDTH, HEIGHT)

# --------------------
# COLORS
# --------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# --------------------
# PLAYER
# --------------------
player_width, player_height = 50, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 70
player_speed = 6

# --------------------
# PLAYER HEALTH & LIVES
# --------------------
player_max_hp = 100
player_hp = 100
player_lives = 3

last_hit_time = 0
invincible_duration = 1000  # ms
damage_per_hit = 20

# --------------------
# BULLETS
# --------------------
bullets = []
bullet_speed = 8

# --------------------
# ENEMIES
# --------------------
enemies = []
enemy_speed = 3
# spawn_timer = 0

# --------------------
# SCORE
# --------------------
score = 0
font = pygame.font.SysFont(None, 36)

# --------------------
# DRAW FUNCTIONS
# --------------------
def draw_player(x, y):
    pygame.draw.polygon(
        screen,
        WHITE,
        [
            (x, y + player_height),
            (x + player_width // 2, y),
            (x + player_width, y + player_height),
        ],
    )

def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
# --------------------
# GAME LOOP
# --------------------

running = True
while running:
    clock.tick(60)
    
    # --------------------
    # EVENTS
    # --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x + player_width // 2 - 3,player_y,6,12,))
                sound.play_shoot()
           # if event.type == randomize_dodging:
           # randomize_dodging()
    # --------------------
    # INPUT
    # --------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # --------------------
    # DRAW BACKGROUND
    # --------------------
    bg.draw(screen)

    # --------------------
    # BULLET UPDATE
    # --------------------
    spawn_timer =0
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # --------------------
    # ENEMY SPAWN
    # --------------------
    spawn_timer += 1
    if spawn_timer > 40:
        enemies.append(pygame.Rect(random.randint(0,WIDTH -40), -40, 40, 30))      
        # Smarter_enemies.spawn_enemy(enemies, WIDTH)
        spawn_timer = 0
        if score > 3:
            spawn_timer = 20
            enemies.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 30))
            spawn_timer = 0 
    # --------------------
    # ENEMY UPDATE (SMART AI)
    # --------------------
    score = Smarter_enemies.update_enemies(
        enemies=enemies,
        bullets=bullets,
        enemy_speed=enemy_speed,
        score=score,
        sound=sound,
        screen_height=HEIGHT,
    )

    # --------------------
    # PLAYER VS ENEMY COLLISION
    # --------------------
    player_rect = pygame.Rect(
        player_x, player_y, player_width, player_height
    )
    current_time = pygame.time.get_ticks()

    for enemy in enemies[:]:
        if player_rect.colliderect(enemy):
            if current_time - last_hit_time > invincible_duration:
                player_hp -= damage_per_hit
                last_hit_time = current_time
                enemies.remove(enemy)

    # --------------------
    # DEATH & RESPAWN
    # --------------------
    if player_hp <= 0:
        player_lives -= 1

        if player_lives > 0:
            player_hp = player_max_hp
            player_x = WIDTH // 2 - player_width // 2
            player_y = HEIGHT - 70
            enemies.clear()
            bullets.clear()
            pygame.time.delay(1000)
        else:
            print("GAME OVER")
            running = False

    # --------------------
    # DRAW PLAYER (INVINCIBILITY FLASH)
    # --------------------
    if current_time - last_hit_time < invincible_duration:
        if (current_time // 100) % 2 == 0:
            draw_player(player_x, player_y)
    else:
        draw_player(player_x, player_y)

    # --------------------
    # DRAW BULLETS & ENEMIES
    # --------------------
    for bullet in bullets[:]:
        #     def randomize_dodging():
        #     randomize_dodging = pygame.USEREVENT + 0
        #     pygame.time.set_timer(randomize_dodging, 5000)
            bullet_is_threatening = False
            dodge_to_right = enemy.x + 10
            dodge_to_left = enemy.x - 10
            danger_width = enemy.width
            if abs(bullet.x - enemy.x) < danger_width:

                # bullet_is_threatening = True
            # if abs(bullet.centerx-enemy.centerx)< danger_width and bullet.y < enemy.y:
                bullet_is_threatening = True 
            if bullet_is_threatening ==True:
                if dodges > 0:
                    choice = choices ([dodge_to_right, dodge_to_left], [0.5, 0.5])[0] 
                    enemy.x = choice 
                dodges = dodges - 1
            # randomize_dodging()
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break
        # pygame.draw.rect(screen, WHITE, bullet)
    for enemy in enemies[:]:
        dodges = 1
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)      
        pygame.draw.rect(screen, RED, enemy)

    # --------------------
    # UI (HEALTH, LIVES, SCORE)
    # --------------------
    health.draw_health_bar(
        screen, 10, 10, player_hp, player_max_hp
    )
    health.draw_lives(
        screen, 10, 40, player_lives, font
    )

    score_text = font.render(
        f"Score: {score}", True, WHITE
    )
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.flip()

pygame.quit()
