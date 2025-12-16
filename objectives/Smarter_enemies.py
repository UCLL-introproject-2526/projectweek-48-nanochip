# Simple Spaceship Game using Pygame
# Run with: python app.py
import math
import pygame
import random
from random import choices

def spawn_enemy(enemies, width):
    enemies.append(
        pygame.Rect(random.randint(0, width - 40), -40, 40, 30)
    )

def update_enemies(
    enemies,
    bullets,
    enemy_speed,
    score,
    sound,
    screen_height
):
    """
    Handles:
    - Enemy movement
    - Dodging bullets
    - Bullet collision
    Returns updated score
    """

def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# --------------------
# GAME LOOP
# --------------------
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x + player_width // 2 - 3, player_y, 6, 12))
        # if event.type == randomize_dodging:
        #     randomize_dodging()
    # INPUT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # BULLETS UPDATE
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)


    # ENEMY SPAWN
    spawn_timer += 1
    spawn_delay = 40
    if spawn_timer > spawn_delay:
        # t = pygame.time.get_ticks() / 2 % 400
        # x = t
        # y = math.sin(t/50.0) * 100 + 200
        # y = int(y)
        # print(y)
        enemies.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 30))
        # enemies.append(pygame.Rect(x, y), -40, 40, 30)


        spawn_timer = 0

    if score > 10:
        # spawn_timer = 0 
        spawn_delay = 20
        if spawn_timer > spawn_delay:
            enemies.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 30))
            spawn_timer = 0 
   # ENEMY UPDATE
    for enemy in enemies[:]:
        enemy.y += enemy_speed

        if enemy.y > screen_height:
            enemies.remove(enemy)
            continue

        dodges = 1

        for bullet in bullets[:]:
            bullet_is_threatening = (
                abs(bullet.centerx - enemy.centerx) < enemy.width
                and bullet.y < enemy.y
            )

            if bullet_is_threatening and dodges > 0:
                dodge = choices(
                    [enemy.x - 15, enemy.x + 15],
                    [0.5, 0.5]
                )[0]
                enemy.x = dodge
                dodges -= 1

            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                sound.play_explosion()
                score += 1
                break

    return score
