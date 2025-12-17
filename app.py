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
<<<<<<< HEAD
pygame.display.set_caption("Spaceship Game - Sector 48")
clock = pygame.time.Clock()

# --------------------
# COLORS & FONT
# --------------------
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# --------------------
# CONFIG VARIABLES
# --------------------
player_width, player_height = 50, 40
player_speed = 6
player_max_hp = 100
damage_per_hit = 20
base_invincible_duration = 1000

# Enemy Defaults
base_enemy_speed = 3
spawn_rate = 40 

# --------------------
# GAME LISTS
# --------------------
bullets = []
enemies = []
explosions = []
powerups = []
spawn_timer = 0

# --------------------
# GAME STATE
# --------------------
GAME_RUNNING = "running"
GAME_OVER = "over"
GAME_PAUSED = "paused" # <--- NEW STATE
game_state = GAME_RUNNING

# --------------------
# SHAKE EFFECT
# --------------------
screen_shake = 0 # Timer for shake

# --------------------
# BACKGROUND & ASSETS
=======
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()

# --------------------
# BACKGROUND
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5
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
<<<<<<< HEAD

# Buffs
rapid_fire_active = False
rapid_fire_end_time = 0
shield_active = False
shield_end_time = 0
shield_angle = 0

# LEVEL SYSTEM VARIABLES
level = 1
next_level_score = 150
current_boss = None
=======
invincible_duration = 1000  # ms
damage_per_hit = 20
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5

# --------------------
# BULLETS
# --------------------
<<<<<<< HEAD
def reset_game():
    global player_x, player_y, player_hp, player_lives
    global bullets, enemies, explosions, powerups
    global score, spawn_timer, last_hit_time, game_state
    global rapid_fire_active, shield_active, shield_angle
    global level, next_level_score, current_boss, spawn_rate, screen_shake

    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 70
    player_hp = player_max_hp
    player_lives = 3

    bullets.clear()
    enemies.clear()
    explosions.clear()
    powerups.clear()

    score = 0
    spawn_timer = 0
    last_hit_time = 0
    screen_shake = 0

    rapid_fire_active = False
    shield_active = False
    shield_angle = 0

    # Reset Levels
    level = 1
    next_level_score = 150
    current_boss = None
    spawn_rate = 40

    sound.play_background_music()
    game_state = GAME_RUNNING
=======
bullets = []
bullet_speed = 8
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5

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
<<<<<<< HEAD
    current_time = pygame.time.get_ticks()

    # 1. EVENTS (Includes Pause Toggle)
=======
    
    # --------------------
    # EVENTS
    # --------------------
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
<<<<<<< HEAD
            # PAUSE TOGGLE
            if event.key == pygame.K_p:
                if game_state == GAME_RUNNING:
                    game_state = GAME_PAUSED
                    pygame.mixer.music.pause()
                elif game_state == GAME_PAUSED:
                    game_state = GAME_RUNNING
                    pygame.mixer.music.unpause()

            # SHOOTING (Only if running)
            if game_state == GAME_RUNNING and event.key == pygame.K_SPACE:
                center_x = player_x + player_width // 2 - 3
                if rapid_fire_active:
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 0, -12])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), -3, -10])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 3, -10])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), -6, -8])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 6, -8])
                else:
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 0, -8])
                sound.play_shoot()

    # 2. PAUSE LOGIC
    if game_state == GAME_PAUSED:
        pause_text = big_font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
        pygame.display.flip()
        continue # Skip the rest of the loop while paused

    # 3. GAME OVER LOGIC
    if game_state == GAME_OVER:
        action = game_over_screen(screen, clock)
        if action == "restart":
            reset_game()
        continue

    # 4. CALCULATE SHAKE OFFSET
    shake_x, shake_y = 0, 0
    if screen_shake > 0:
        screen_shake -= 1
        shake_x = random.randint(-5, 5)
        shake_y = random.randint(-5, 5)

    # 5. LEVEL UP LOGIC
    if score >= next_level_score and current_boss is None:
        if (level + 1) in [5, 10, 15, 20]:
            level += 1
            # SPAWN BOSS (Pass both WIDTH and HEIGHT)
            current_boss = boss_module.Boss(WIDTH, HEIGHT)
            current_boss.max_hp = 500 + (level * 100) 
            current_boss.hp = current_boss.max_hp
            enemies.clear() 
        else:
            level += 1
            next_level_score = level * 150
            spawn_rate = max(10, 40 - level)
            print(f"LEVEL UP! Welcome to Level {level}")

    # TIMERS
    if rapid_fire_active and current_time > rapid_fire_end_time:
        rapid_fire_active = False
    
    if shield_active:
        if current_time > shield_end_time:
            shield_active = False
        else:
            shield_angle += 5
            if shield_angle >= 360: shield_angle -= 360

    # MOVEMENT
=======
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x + player_width // 2 - 3,player_y,6,12,))
                sound.play_shoot()
           # if event.type == randomize_dodging:
           # randomize_dodging()
    # --------------------
    # INPUT
    # --------------------
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

<<<<<<< HEAD
    # DRAW BACKGROUND (Apply Shake)
    # We access the image directly to apply the offset
    screen.blit(bg.image, (shake_x, shake_y))
=======
    # --------------------
    # DRAW BACKGROUND
    # --------------------
    bg.draw(screen)
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5

    # --------------------
    # BULLET UPDATE
    # --------------------
    spawn_timer =0
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

<<<<<<< HEAD
    # ---------------------------
    # SPAWN & UPDATE ENEMIES OR BOSS
    # ---------------------------
    if current_boss is None:
        spawn_timer += 1
        if spawn_timer > spawn_rate: 
            smarter_enemies.spawn_enemy(enemies, WIDTH, 50, 40)
            spawn_timer = 0
            
        current_enemy_speed = base_enemy_speed + (level * 0.2)
        score = smarter_enemies.update_enemies(
            enemies=enemies,
            bullets=bullets,
            enemy_speed=current_enemy_speed,
            score=score,
            sound=sound,
            screen_height=HEIGHT,
            explosions=explosions,
            player_x=player_x,
            player_y=player_y,
            powerups_list=powerups
        )
    else:
        # BOSS LOGIC
        current_boss.update() 
        # Draw Boss with Shake
        screen.blit(current_boss.image, (current_boss.rect.x + shake_x, current_boss.rect.y + shake_y))

        current_boss.bullets.update()
        current_boss.bullets.draw(screen)

        # Check collision: Boss Bullets vs Player
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for bullet in current_boss.bullets:
            if player_rect.colliderect(bullet.rect):
                bullet.kill()
                if not shield_active:
                    if current_time - last_hit_time > base_invincible_duration:
                        player_hp -= 15
                        last_hit_time = current_time
                        sound.play_explosion()

        # Check collision: Player Bullets vs Boss
        for b_data in bullets[:]:
            rect = b_data[0]
            if rect.colliderect(current_boss.rect):
                current_boss.hp -= 10
                explosions.append(Explosion(rect.x, rect.y))
                bullets.remove(b_data)
                
                # BOSS DEATH
                if current_boss.hp <= 0:
                    score += 500 
                    next_level_score = score + 150 
                    sound.play_explosion()
                    
                    # TRIGGER SHAKE
                    screen_shake = 30 
                    
                    # Spawn Rewards
                    try:
                        powerups_module.spawn_powerup_at(powerups, current_boss.rect.centerx, current_boss.rect.centery)
                        powerups_module.spawn_powerup_at(powerups, current_boss.rect.centerx + 40, current_boss.rect.centery)
                        powerups_module.spawn_powerup_at(powerups, current_boss.rect.centerx - 40, current_boss.rect.centery)
                    except AttributeError:
                        pass
                    current_boss = None 
                break
        
        # Check collision: Player vs Boss Body
        if current_boss and player_rect.colliderect(current_boss.rect):
            if not shield_active:
                if current_time - last_hit_time > base_invincible_duration:
                     player_hp -= 30 
                     last_hit_time = current_time
                     sound.play_explosion()

        # Random Powerup Drop during Boss Fight
        if random.randint(1, 100) <= 2:
             drop_x = random.randint(50, WIDTH - 50)
             try:
                 powerups_module.spawn_powerup_at(powerups, drop_x, -50)
             except AttributeError:
                 pass

    # POWERUPS
    for p in powerups[:]:
        p.update()
        p.draw(screen)
        
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if player_rect.colliderect(p.rect):
            if p.type == powerups_module.EXTRA_LIFE:
                if player_lives < 5: player_lives += 1
            elif p.type == powerups_module.RAPID_FIRE:
                rapid_fire_active = True
                rapid_fire_end_time = current_time + 5000
            elif p.type == powerups_module.SHIELD:
                shield_active = True
                shield_end_time = current_time + 5000
            powerups.remove(p)
        elif p.rect.y > HEIGHT:
            powerups.remove(p)

    # COLLISION PLAYER (Normal Enemies)
    if current_boss is None:
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for enemy in enemies[:]:
            if player_rect.colliderect(enemy):
                if shield_active:
                    explosions.append(Explosion(enemy.x + 25, enemy.y + 20))
                    enemies.remove(enemy)
                    sound.play_explosion()
                else:
                    if current_time - last_hit_time > base_invincible_duration:
                        player_hp -= damage_per_hit
                        last_hit_time = current_time
                        explosions.append(Explosion(enemy.x + 25, enemy.y + 20))
                        enemies.remove(enemy)
                        sound.play_explosion()

    # CHECK DEATH
=======
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
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5
    if player_hp <= 0:
        player_lives -= 1

        if player_lives > 0:
            player_hp = player_max_hp
            player_x = WIDTH // 2 - player_width // 2
            player_y = HEIGHT - 70
            enemies.clear()
            bullets.clear()
<<<<<<< HEAD
            explosions.clear()
            powerups.clear()
            rapid_fire_active = False
            shield_active = False
            current_boss = None
            screen_shake = 0
            pygame.time.delay(800)
=======
            pygame.time.delay(1000)
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5
        else:
            print("GAME OVER")
            running = False

<<<<<<< HEAD
    # DRAW PLAYER (With Shake)
    is_hit_invincible = (current_time - last_hit_time < base_invincible_duration)
    if is_hit_invincible and not shield_active:
=======
    # --------------------
    # DRAW PLAYER (INVINCIBILITY FLASH)
    # --------------------
    if current_time - last_hit_time < invincible_duration:
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5
        if (current_time // 100) % 2 == 0:
            draw_player(player_x + shake_x, player_y + shake_y)
    else:
        draw_player(player_x + shake_x, player_y + shake_y)

<<<<<<< HEAD
    # DRAW BULLETS
    for b_data in bullets:
        rect = b_data[0]
        # Create a temp rect for drawing with shake offset
        draw_rect = rect.move(shake_x, shake_y)
        b_color = (255, 255, 0) if rapid_fire_active else WHITE
        pygame.draw.rect(screen, b_color, draw_rect)

    # DRAW ENEMIES (With Shake)
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x + shake_x, enemy.y + shake_y))
=======
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
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5

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

<<<<<<< HEAD
    level_text = font.render(f"LEVEL {level}", True, CYAN)
    screen.blit(level_text, (WIDTH // 2 - 50, 10))
    
    if current_boss:
        warn_text = big_font.render("BOSS FIGHT!", True, RED)
        screen.blit(warn_text, (WIDTH // 2 - 140, HEIGHT // 2))

    if rapid_fire_active:
        rf_text = font.render("RAPID FIRE!", True, CYAN)
        screen.blit(rf_text, (WIDTH//2 - 60, HEIGHT - 40))
        
    if shield_active:
        sh_text = font.render("SHIELD ACTIVE", True, (255, 255, 0))
        y_pos = HEIGHT - 70 if rapid_fire_active else HEIGHT - 40
        screen.blit(sh_text, (WIDTH//2 - 60, y_pos))

=======
>>>>>>> 947139c5ed2e445cf7493e1851e3bc0e394125c5
    pygame.display.flip()

pygame.quit()
