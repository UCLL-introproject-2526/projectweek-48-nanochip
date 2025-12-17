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

<<<<<<< HEAD
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
=======
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
>>>>>>> 59ad1a7da44aac9883fc20723321a1543bebafad
