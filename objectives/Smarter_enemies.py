# Simple Spaceship Game using Pygame
# Run with: python app.py
import math
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
