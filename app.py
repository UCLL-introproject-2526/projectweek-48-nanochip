import pygame
import sys
import random
import os
import math

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
import objectives.powerup as powerups_module
import objectives.boss as boss_module

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
pygame.display.set_caption("Spaceship Game - Levels & Bosses")
clock = pygame.time.Clock()

# --------------------
# COLORS & FONT
# --------------------
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)   # Important for UI text
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
game_state = GAME_RUNNING

# --------------------
# BACKGROUND & ASSETS
# --------------------
bg = Background("spaceship.jpg", WIDTH, HEIGHT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

player_img_path = os.path.join(BASE_DIR, "objectives", "images", "player_ship.png")
enemy_img_path = os.path.join(BASE_DIR, "objectives", "images", "enemy_ship.png")

# Load Images (Fallback logic)
try:
    player_img = pygame.image.load(player_img_path).convert_alpha()
    player_img = pygame.transform.scale(player_img, (player_width, player_height))
except FileNotFoundError:
    player_img = pygame.Surface((player_width, player_height))
    player_img.fill((0, 255, 0))

try:
    enemy_img = pygame.image.load(enemy_img_path).convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (50, 40))
except FileNotFoundError:
    enemy_img = pygame.Surface((50, 40))
    enemy_img.fill((255, 0, 0))

# --------------------
# VARIABLES
# --------------------
player_x = 0
player_y = 0
player_hp = 0
player_lives = 0
score = 0
last_hit_time = 0

# Buffs
rapid_fire_active = False
rapid_fire_end_time = 0
shield_active = False
shield_end_time = 0
shield_angle = 0

# LEVEL SYSTEM VARIABLES
level = 1
next_level_score = 150
current_boss = None  # Will hold the Boss object when active

# --------------------
# RESET GAME
# --------------------
def reset_game():
    global player_x, player_y, player_hp, player_lives
    global bullets, enemies, explosions, powerups
    global score, spawn_timer, last_hit_time, game_state
    global rapid_fire_active, shield_active, shield_angle
    global level, next_level_score, current_boss, spawn_rate

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

# --------------------
# DRAW PLAYER
# --------------------
def draw_player(x, y):
    if shield_active:
        center_x = x + player_width // 2
        center_y = y + player_height // 2
        radius = 40
        pygame.draw.circle(screen, (0, 100, 100), (center_x, center_y), radius, 1)
        # Rotating Orbs
        num_orbiters = 3
        for i in range(num_orbiters):
            offset = (360 / num_orbiters) * i
            rad_angle = math.radians(shield_angle + offset)
            orb_x = center_x + math.cos(rad_angle) * radius
            orb_y = center_y + math.sin(rad_angle) * radius
            pygame.draw.circle(screen, WHITE, (int(orb_x), int(orb_y)), 4)
            pygame.draw.circle(screen, CYAN, (int(orb_x), int(orb_y)), 2)

    screen.blit(player_img, (x, y))

# --------------------
# START MENU
# --------------------
action = start_menu.start_menu(screen, clock)
if action == "start":
    reset_game()
elif action == "quit":
    pygame.quit()
    sys.exit()

# --------------------
# MAIN LOOP
# --------------------
running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    # 1. LEVEL UP LOGIC
    # Check if we reached score threshold AND we are not currently fighting a boss
    if score >= next_level_score and current_boss is None:
        
        # Check if next level is a BOSS LEVEL (5, 10, 15, 20)
        if (level + 1) in [5, 10, 15, 20]:
            level += 1
            # SPAWN BOSS (Pass both WIDTH and HEIGHT)
            current_boss = boss_module.Boss(WIDTH, HEIGHT)
            
            # BOSS HP (Fixed math to prevent 0 HP crash at level 4/5)
            current_boss.max_hp = 500 + (level * 100) 
            current_boss.hp = current_boss.max_hp
            
            enemies.clear() # Clear small enemies
        else:
            # Normal Level Up
            level += 1
            next_level_score = level * 150
            # Increase Difficulty
            spawn_rate = max(10, 40 - level)
            print(f"LEVEL UP! Welcome to Level {level}")

    # 2. EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == GAME_RUNNING and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # SHOOTING
                center_x = player_x + player_width // 2 - 3
                if rapid_fire_active:
                    # Spray Shot
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 0, -12])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), -3, -10])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 3, -10])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), -6, -8])
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 6, -8])
                else:
                    bullets.append([pygame.Rect(center_x, player_y, 6, 12), 0, -8])
                
                sound.play_shoot()

    # GAME OVER LOGIC
    if game_state == GAME_OVER:
        action = game_over_screen(screen, clock)
        if action == "restart":
            reset_game()
        continue

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
    keys = pygame.key.get_pressed()
    current_speed = player_speed + 2 if rapid_fire_active else player_speed
    
    if keys[pygame.K_LEFT]:
        player_x -= current_speed
        if player_x + player_width < 0: player_x = WIDTH
    if keys[pygame.K_RIGHT]:
        player_x += current_speed
        if player_x > WIDTH: player_x = -player_width

    # DRAW BACKGROUND
    bg.draw(screen)

    # UPDATE PLAYER BULLETS
    for b_data in bullets[:]:
        rect = b_data[0]
        rect.x += b_data[1]
        rect.y += b_data[2]
        if rect.y < 0 or rect.x < 0 or rect.x > WIDTH:
            bullets.remove(b_data)

    # ---------------------------
    # SPAWN & UPDATE ENEMIES OR BOSS
    # ---------------------------
    
    # Only spawn normal enemies if NO BOSS is active
    if current_boss is None:
        spawn_timer += 1
        if spawn_timer > spawn_rate: 
            smarter_enemies.spawn_enemy(enemies, WIDTH, 50, 40)
            spawn_timer = 0
            
        # Update Normal Enemies
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
        # ==========================================
        # BOSS FIGHT LOGIC
        # ==========================================
        
        # 1. Update Boss
        current_boss.update() 
        
        # 2. Draw Boss (Using blit because boss is a single Sprite, not a group)
        screen.blit(current_boss.image, current_boss.rect)

        # 3. Boss Shooting
        current_boss.bullets.update()
        current_boss.bullets.draw(screen)

        # 4. Check collision: Boss Bullets vs Player
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
        for bullet in current_boss.bullets:
            if player_rect.colliderect(bullet.rect):
                bullet.kill() # Remove bullet
                if not shield_active:
                    # Only take damage if not invincible
                    if current_time - last_hit_time > base_invincible_duration:
                        player_hp -= 15
                        last_hit_time = current_time
                        sound.play_explosion()
                        print("Hit by Boss Bullet!")

        # 5. Check collision: Player Bullets vs Boss
        for b_data in bullets[:]:
            rect = b_data[0]
            if rect.colliderect(current_boss.rect):
                current_boss.hp -= 10 # Damage to boss
                explosions.append(Explosion(rect.x, rect.y))
                bullets.remove(b_data)
                
                # Check Boss Death
                if current_boss.hp <= 0:
                    score += 500 
                    next_level_score = score + 150 
                    sound.play_explosion()
                    
                    # Reward: Spawn Powerups
                    # We use the helper function from powerup.py
                    try:
                        powerups_module.spawn_powerup_at(powerups, current_boss.rect.centerx, current_boss.rect.centery)
                        powerups_module.spawn_powerup_at(powerups, current_boss.rect.centerx + 40, current_boss.rect.centery)
                        powerups_module.spawn_powerup_at(powerups, current_boss.rect.centerx - 40, current_boss.rect.centery)
                    except AttributeError:
                        # Fallback if function name is different
                        pass

                    current_boss = None 
                break
        
        # 6. Check collision: Player vs Boss Body
        if current_boss and player_rect.colliderect(current_boss.rect):
            if not shield_active:
                if current_time - last_hit_time > base_invincible_duration:
                     player_hp -= 30 
                     last_hit_time = current_time
                     sound.play_explosion()

        # 7. Random Powerup Drop during Boss Fight
        if random.randint(1, 100) <= 2: # 2% chance per frame
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
    if player_hp <= 0:
        player_lives -= 1
        if player_lives > 0:
            player_hp = player_max_hp
            enemies.clear()
            bullets.clear()
            explosions.clear()
            powerups.clear()
            rapid_fire_active = False
            shield_active = False
            current_boss = None
            pygame.time.delay(800)
        else:
            sound.stop_background_music()
            sound.play_game_over()
            game_state = GAME_OVER

    # DRAW PLAYER
    is_hit_invincible = (current_time - last_hit_time < base_invincible_duration)
    if is_hit_invincible and not shield_active:
        if (current_time // 100) % 2 == 0:
            draw_player(player_x, player_y)
    else:
        draw_player(player_x, player_y)

    # DRAW BULLETS
    for b_data in bullets:
        rect = b_data[0]
        b_color = (255, 255, 0) if rapid_fire_active else WHITE
        pygame.draw.rect(screen, b_color, rect)

    # DRAW ENEMIES
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))

    # DRAW EXPLOSIONS
    for exp in explosions[:]:
        exp.update()
        exp.draw(screen)
        if exp.is_dead():
            explosions.remove(exp)

    # UI
    health.draw_health_bar(screen, 10, 10, player_hp, player_max_hp)
    health.draw_lives(screen, 10, 40, player_lives, font)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

    # DISPLAY LEVEL
    level_text = font.render(f"LEVEL {level}", True, CYAN)
    screen.blit(level_text, (WIDTH // 2 - 50, 10))
    
    # DISPLAY BOSS WARNING
    if current_boss:
        warn_text = big_font.render("BOSS FIGHT!", True, RED)
        screen.blit(warn_text, (WIDTH // 2 - 140, HEIGHT // 2))

    # BUFF TEXT
    if rapid_fire_active:
        rf_text = font.render("RAPID FIRE!", True, CYAN)
        screen.blit(rf_text, (WIDTH//2 - 60, HEIGHT - 40))
        
    if shield_active:
        sh_text = font.render("SHIELD ACTIVE", True, (255, 255, 0))
        y_pos = HEIGHT - 70 if rapid_fire_active else HEIGHT - 40
        screen.blit(sh_text, (WIDTH//2 - 60, y_pos))

    pygame.display.flip()

pygame.quit()