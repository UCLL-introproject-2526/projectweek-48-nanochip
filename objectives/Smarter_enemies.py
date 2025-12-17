# import pygame
# import random
# # [FIX] Import matched to your filename 'powerup.py'
# import objectives.powerup as powerup_mod 

# def spawn_enemy(enemies, width, enemy_width, enemy_height):
#     """Generates a random enemy"""
#     x_pos = random.randint(0, width - enemy_width)
#     enemies.append(pygame.Rect(x_pos, -enemy_height, enemy_width, enemy_height))

# def update_enemies(enemies, bullets, enemy_speed, score, sound, screen_height, explosions, player_x, player_y, powerups_list):
#     """
#     Updates enemy positions, checks collisions, and SPAWNS POWERUPS.
#     """
#     for enemy in enemies[:]:
#         # 1. Move Enemy
#         enemy.y += enemy_speed

#         # Simple AI: Chase player X slightly
#         if enemy.centerx < player_x:
#             enemy.x += 1
#         elif enemy.centerx > player_x:
#             enemy.x -= 1

#         # Remove if off screen
#         if enemy.y > screen_height:
#             enemies.remove(enemy)
#             continue

#         # 2. Check Collision with Bullets
#         enemy_hit = False
#         for bullet in bullets[:]:
#             if enemy.colliderect(bullet):
#                 # --- ENEMY DEATH LOGIC ---
                
#                 # A. Explosion Effect
#                 # We import locally to avoid circular import errors
#                 from objectives.explosion import Explosion 
#                 if explosions is not None:
#                     explosions.append(Explosion(enemy.centerx, enemy.centery))
                
#                 # B. [NEW] Spawn Power-up 
#                 # This was missing in your screenshot!
#                 powerup_mod.spawn_powerup_at(powerups_list, enemy.x, enemy.y)

#                 # C. Remove bullet and enemy
#                 try:
#                     bullets.remove(bullet)
#                     enemies.remove(enemy)
#                 except ValueError:
#                     pass # Prevent crash if already removed
                
#                 # D. Score & Sound
#                 score += 10
#                 if sound:
#                     sound.play_explosion()
                
#                 enemy_hit = True
#                 break # Stop checking bullets for this enemy
        
#         if enemy_hit:
#             continue

#     return score

import pygame
import random
import objectives.powerup as powerup_mod 

def spawn_enemy(enemies, width, enemy_width, enemy_height):
    x_pos = random.randint(0, width - enemy_width)
    enemies.append(pygame.Rect(x_pos, -enemy_height, enemy_width, enemy_height))

def update_enemies(enemies, bullets, enemy_speed, score, sound, screen_height, explosions, player_x, player_y, powerups_list):
    for enemy in enemies[:]:
        # 1. Move Enemy
        enemy.y += enemy_speed
        if enemy.centerx < player_x: enemy.x += 1
        elif enemy.centerx > player_x: enemy.x -= 1

        if enemy.y > screen_height:
            enemies.remove(enemy)
            continue

        # 2. Check Collision with Bullets
        enemy_hit = False
        for bullet_data in bullets[:]:
            # CRITICAL CHANGE: bullet_data is now [Rect, SpeedX, SpeedY]
            # So we use bullet_data[0] to get the Rectangle
            bullet_rect = bullet_data[0] 

            if enemy.colliderect(bullet_rect):
                from objectives.explosion import Explosion 
                if explosions is not None:
                    explosions.append(Explosion(enemy.centerx, enemy.centery))
                
                powerup_mod.spawn_powerup_at(powerups_list, enemy.x, enemy.y)

                try:
                    bullets.remove(bullet_data) # Remove the whole bullet data
                    enemies.remove(enemy)
                except ValueError:
                    pass 
                
                score += 10
                if sound: sound.play_explosion()
                enemy_hit = True
                break 
        
        if enemy_hit: continue

    return score