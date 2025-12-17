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
