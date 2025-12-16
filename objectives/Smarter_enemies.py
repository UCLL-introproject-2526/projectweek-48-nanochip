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
