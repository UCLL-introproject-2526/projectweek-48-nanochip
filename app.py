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


# --------------------
# DISPLAY
# --------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game - Sector 48")
clock = pygame.time.Clock()
# remember last known windowed size so ESC can restore/center
last_windowed_size = (WIDTH, HEIGHT)

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
BOSS_TARGET_Y = 70  # Y position where boss settles after intro

# --------------------
# HIGH SCORE SYSTEM
# --------------------
HIGHSCORE_FILE = "highscore.txt"

def load_high_score():
    """Loads the high score from a file, returns 0 if file doesn't exist."""
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except:
            return 0
    return 0

def save_high_score(new_best):
    """Saves the new high score to the file."""
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(new_best))
    except:
        print("Could not save high score.")

# Initialize High Score
high_score = load_high_score()

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
GAME_PAUSED = "paused"
game_state = GAME_RUNNING

# --------------------
# SHAKE EFFECT
# --------------------
screen_shake = 0

# --------------------
# BACKGROUND & ASSETS (deferred load to speed startup)
# --------------------
bg = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
player_img = None
enemy_img = None
player_img_path = os.path.join(BASE_DIR, "objectives", "images", "player_ship.png")
enemy_img_path = os.path.join(BASE_DIR, "objectives", "images", "enemy_ship.png")

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
current_boss = None

# BOSS INTRO / CINEMATIC
boss_intro = False
boss_intro_start = 0
boss_intro_duration = 2000    # ms
boss_bar_height = 80

# --------------------
# RESET GAME
# --------------------
def reset_game():
    global player_x, player_y, player_hp, player_lives
    global bullets, enemies, explosions, powerups
    global score, spawn_timer, last_hit_time, game_state
    global rapid_fire_active, shield_active, shield_angle
    global level, next_level_score, current_boss, spawn_rate, screen_shake
    global high_score, boss_intro, boss_intro_start, boss_bar_height

    # Reload high score
    high_score = load_high_score()

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
    
    # Reset Boss Intro vars
    boss_intro = False
    boss_intro_start = 0
    boss_bar_height = 80

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
# start_menu may change display mode (fullscreen). it returns (action, is_fullscreen)
res = start_menu.start_menu(screen, clock)
if isinstance(res, tuple) and len(res) == 2:
    action, is_fullscreen = res
else:
    action = res
    is_fullscreen = False

# refresh display surface and sizes in case mode changed in menu
screen = pygame.display.get_surface()
WIDTH, HEIGHT = screen.get_size()
if not is_fullscreen:
    last_windowed_size = (WIDTH, HEIGHT)
    
# compute scale factor from original design (800x600)
scale_x = WIDTH / 800.0
scale_y = HEIGHT / 600.0

# scale player/enemy sizes to fit the new window
player_width = max(16, int(50 * scale_x))
player_height = max(12, int(40 * scale_y))

# Load images now if they were deferred
try:
    if player_img is None:
        try:
            player_img = pygame.image.load(player_img_path).convert_alpha()
        except Exception:
            player_img = pygame.Surface((player_width, player_height))
            player_img.fill((0, 255, 0))
    if enemy_img is None:
        try:
            enemy_img = pygame.image.load(enemy_img_path).convert_alpha()
        except Exception:
            enemy_img = pygame.Surface((50, 40))
            enemy_img.fill((255, 0, 0))
except Exception:
    pass

try:
    # rescale player image to new size
    player_img = pygame.transform.scale(player_img, (player_width, player_height))
except Exception:
    pass
try:
    enemy_w = max(16, int(50 * scale_x))
    enemy_h = max(12, int(40 * scale_y))
    enemy_img = pygame.transform.scale(enemy_img, (enemy_w, enemy_h))
except Exception:
    pass

# recreate background to match new size
bg = Background("spaceship.jpg", WIDTH, HEIGHT)

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

    # 1. EVENTS (Includes Pause Toggle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # ESC should restore or center window (mid-screen)
            if event.key == pygame.K_ESCAPE:
                try:
                    info = pygame.display.Info()
                    surf = pygame.display.get_surface()
                    flags = surf.get_flags()
                    # if fullscreen -> restore to last windowed size, else keep current
                    if flags & pygame.FULLSCREEN:
                        win_w, win_h = last_windowed_size
                    else:
                        win_w, win_h = surf.get_size()

                    pos_x = max(0, (info.current_w - win_w) // 2)
                    pos_y = max(0, (info.current_h - win_h) // 2)
                    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{pos_x},{pos_y}"
                    pygame.display.set_mode((win_w, win_h))
                    # refresh surfaces and sizes
                    screen = pygame.display.get_surface()
                    WIDTH, HEIGHT = screen.get_size()
                    # update last windowed size
                    last_windowed_size = (WIDTH, HEIGHT)
                    try:
                        bg = Background("spaceship.jpg", WIDTH, HEIGHT)
                    except Exception:
                        pass
                except Exception:
                    pass
                continue
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

    # 3. GAME OVER LOGIC (Updated with Scores)
    if game_state == GAME_OVER:
        # Check and Save High Score
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        # Call the new game_over_screen with score arguments
        action = game_over_screen(screen, clock, score, high_score)
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
        # If the next level is a boss level, prepare and spawn a boss
        if (level + 1) in [5, 10, 15, 20]:
            level += 1
            variant_name = None
            alt_img_path = None

            # Level 5: Demon Boss (stronger boss as requested)
            if level == 5:
                # Prefer a 'demon' themed boss if available. Fallback to other boss images.
                # Level 5: first major boss (prefer hard variants 'sotrak_rewop' or 'stark_rewop')
                if level == 5:
                    for name in ("sotrak_rewop.png", "stark_rewop.png", "alien_boss.png"):
                        path = os.path.join(BASE_DIR, "objectives", "images", name)
                        if os.path.exists(path):
                            variant_name = name.rsplit('.', 1)[0]
                            alt_img_path = path
                            break

            # Level 10: Demon boss (prefer 'demon_boss' here to make second boss more difficult)
            if level == 10:
                for name in ("demon_boss.png", "stark_rewop.png", "alien_boss2.png"):
                    path = os.path.join(BASE_DIR, "objectives", "images", name)
                    if os.path.exists(path):
                        variant_name = name.rsplit('.', 1)[0]
                        alt_img_path = path
                        break

            # Level 15: Final boss (prefer 'final_boss.png')
            if level == 15:
                for name in ("final_boss.png", "demon_boss.png", "alien_boss3.png"):
                    path = os.path.join(BASE_DIR, "objectives", "images", name)
                    if os.path.exists(path):
                        variant_name = name.rsplit('.', 1)[0]
                        alt_img_path = path
                        break



            

            current_boss = boss_module.Boss(WIDTH, HEIGHT, BOSS_TARGET_Y, variant=variant_name)
            current_boss.max_hp = 500 + (level * 100) 
            current_boss.hp = current_boss.max_hp

            # Make certain boss variants tougher
            if variant_name in ("sotrak_rewop", "stark_rewop"):
                # very tough variants
                current_boss.max_hp += 500
                current_boss.hp = current_boss.max_hp
            # Level 5 fallback boss (alien_boss) should be a bit tougher than normal
            if variant_name == "alien_boss":
                current_boss.max_hp += 300
                current_boss.hp = current_boss.max_hp
            # Demon boss: stronger than level-5 variants (level 10 boss)
            if variant_name == "demon_boss":
                current_boss.max_hp += 800
                current_boss.hp = current_boss.max_hp
                # Make it more aggressive at runtime
                try:
                    current_boss.shoot_delay = max(400, current_boss.shoot_delay - 300)
                    current_boss.speed_x = int(current_boss.speed_x * 1.2)
                    current_boss.hard_behavior = True
                except Exception:
                    pass

            enemies.clear()

            # Apply variant image if found
            try:
                if alt_img_path:
                    loaded_img = pygame.image.load(alt_img_path).convert_alpha()
                    current_boss.image = pygame.transform.scale(loaded_img, (current_boss.width, current_boss.height))
                    cx = current_boss.rect.centerx
                    cy = current_boss.rect.centery
                    current_boss.rect = current_boss.image.get_rect()
                    current_boss.rect.centerx = cx
                    current_boss.rect.centery = cy
                else:
                    # Fallback tint
                    try:
                        tinted = current_boss.image.copy()
                        tinted.fill((0, 100, 180, 0), special_flags=pygame.BLEND_RGBA_MULT)
                        current_boss.image = tinted
                    except Exception:
                        pass
            except Exception as e:
                print(f"Warning: Could not set boss variant image: {e}")

            boss_intro = True
            boss_intro_start = pygame.time.get_ticks()
            current_boss.rect.y = -current_boss.rect.height
            sound.stop_background_music()
            sound.play_explosion()
            screen_shake = 10
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
    keys = pygame.key.get_pressed()
    current_speed = player_speed + 2 if rapid_fire_active else player_speed
    
    if keys[pygame.K_LEFT]:
        player_x -= current_speed
        if player_x + player_width < 0: player_x = WIDTH
    if keys[pygame.K_RIGHT]:
        player_x += current_speed
        if player_x > WIDTH: player_x = -player_width

    # DRAW BACKGROUND
    screen.blit(bg.image, (shake_x, shake_y))

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
        if boss_intro:
            elapsed = pygame.time.get_ticks() - boss_intro_start
            t = min(1.0, elapsed / boss_intro_duration)

            # ease-in motion
            ease = t * t
            start_y = -current_boss.rect.height
            target_y = BOSS_TARGET_Y
            current_boss.rect.y = int(start_y + (target_y - start_y) * ease)

            # letterbox bars
            bar_h = int(boss_bar_height * t)
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, bar_h))
            pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - bar_h, WIDTH, bar_h))

            # dark overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(120 * t)))
            screen.blit(overlay, (0, 0))

            # blinking warning
            if (elapsed // 300) % 2 == 0:
                warn = big_font.render("BOSS INCOMING", True, (255, 40, 40))
                screen.blit(warn, (WIDTH // 2 - warn.get_width() // 2, HEIGHT // 2 - 20))

            if elapsed < 50:
                explosions.append(Explosion(WIDTH // 2, 60))

            if elapsed >= boss_intro_duration:
                boss_intro = False
                screen_shake = 6 
                sound.play_background_music()

            # jitter boss during intro
            screen.blit(current_boss.image, (current_boss.rect.x + random.randint(-2, 2), current_boss.rect.y + random.randint(-2, 2)))
        else:
            # normal boss update
            current_boss.update()
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
                    screen_shake = 30 
                    
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
        if not getattr(p, 'picked', False) and player_rect.colliderect(p.rect):
            p.start_pickup()
            try:
                sound.play_explosion()
            except Exception:
                pass

        if getattr(p, 'done', False):
            if p.type == powerups_module.EXTRA_LIFE:
                # Heal one heart (one health segment)
                heal_amount = max(1, player_max_hp // 5)
                player_hp = min(player_max_hp, player_hp + heal_amount)
            elif p.type == powerups_module.RAPID_FIRE:
                rapid_fire_active = True
                rapid_fire_end_time = current_time + 5000
            elif p.type == powerups_module.SHIELD:
                shield_active = True
                shield_end_time = current_time + 5000
            try:
                sound.play_shoot()
            except Exception:
                pass
            powerups.remove(p)
        elif p.rect.y > HEIGHT and not getattr(p, 'picked', False):
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

    # CHECK DEATH: Game Over when HP reaches zero
    if player_hp <= 0:
        sound.stop_background_music()
        sound.play_game_over()
        game_state = GAME_OVER
        if current_boss:
            current_boss.rect.centerx = WIDTH // 2
            current_boss.rect.y = BOSS_TARGET_Y
        screen_shake = 0

    # DRAW PLAYER (With Shake)
    is_hit_invincible = (current_time - last_hit_time < base_invincible_duration)
    if is_hit_invincible and not shield_active:
        if (current_time // 100) % 2 == 0:
            draw_player(player_x + shake_x, player_y + shake_y)
    else:
        draw_player(player_x + shake_x, player_y + shake_y)

    # DRAW BULLETS
    for b_data in bullets:
        rect = b_data[0]
        draw_rect = rect.move(shake_x, shake_y)
        b_color = (255, 255, 0) if rapid_fire_active else WHITE
        pygame.draw.rect(screen, b_color, draw_rect)

    # DRAW ENEMIES (With Shake)
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x + shake_x, enemy.y + shake_y))

    # DRAW EXPLOSIONS
    for exp in explosions[:]:
        exp.update()
        exp.draw(screen)
        if exp.is_dead():
            explosions.remove(exp)

    # UI
    health.draw_health_bar(screen, 10, 10, player_hp, player_max_hp)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

    level_text = font.render(f"LEVEL {level}", True, CYAN)
    screen.blit(level_text, (WIDTH // 2 - 50, 10))
    
    if current_boss:
        bar_width = 400
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = 40
        health.draw_boss_bar(screen, bar_x, bar_y, current_boss.hp, current_boss.max_hp, width=bar_width, height=18, segments=20)
        pct = int(current_boss.hp * 100 / max(1, current_boss.max_hp))
        pct_text = font.render(f"{pct}%", True, RED)
        screen.blit(pct_text, (bar_x + bar_width + 12, bar_y))

    if rapid_fire_active:
        rf_text = font.render("RAPID FIRE!", True, CYAN)
        screen.blit(rf_text, (WIDTH//2 - 60, HEIGHT - 40))
        
    if shield_active:
        sh_text = font.render("SHIELD ACTIVE", True, (255, 255, 0))
        y_pos = HEIGHT - 70 if rapid_fire_active else HEIGHT - 40
        screen.blit(sh_text, (WIDTH//2 - 60, y_pos))

    pygame.display.flip()

pygame.quit()
