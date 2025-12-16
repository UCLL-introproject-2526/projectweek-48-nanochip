# Simple Spaceship Game using Pygame
# Run with: python app.py

import pygame
import random
# --- THÊM DÒNG NÀY: Import file health của bạn ---
from objectives import health  
# -------------------------------------------------

# --------------------
# INIT
# --------------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")
clock = pygame.time.Clock()

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

# --- THÊM: CÁC BIẾN MÁU VÀ MẠNG ---
player_max_hp = 100
player_hp = 100
player_lives = 3

# --- THÊM: BIẾN XỬ LÝ VA CHẠM (BẤT TỬ) ---
last_hit_time = 0         # Thời điểm lần cuối bị đau
invincible_duration = 1000 # Bất tử trong 1000ms (1 giây) sau khi trúng đạn
damage_per_hit = 20       # Mất 20 máu mỗi lần đụng
# ----------------------------------------

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
spawn_timer = 0

# --------------------
# SCORE
# --------------------
score = 0
font = pygame.font.SysFont(None, 36)

def draw_player(x, y):
    pygame.draw.polygon(
        screen,
        WHITE,
        [(x, y + player_height), (x + player_width // 2, y), (x + player_width, y + player_height)]
    )

def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10)) # Sẽ bị trùng với thanh máu, tí mình chỉnh lại vị trí sau

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
    if spawn_timer > 40:
        enemies.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 30))
        spawn_timer = 0

    # --------------------
    # XỬ LÝ LOGIC VA CHẠM (PLAYER VS ENEMY)
    # --------------------
    
    # 1. Tạo hình chữ nhật bao quanh Player để check va chạm
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    
    # 2. Lấy thời gian hiện tại
    current_time = pygame.time.get_ticks()
    
    # ENEMY UPDATE
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            continue # Nếu xóa rồi thì bỏ qua các bước dưới

        # A. COLLISION WITH BULLETS (Đạn bắn kẻ thù)
        bullet_hit = False
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                bullet_hit = True
                break
        
        if bullet_hit: continue # Kẻ thù chết do đạn rồi thì không check va chạm người nữa

        # B. COLLISION WITH PLAYER (Kẻ thù đâm người chơi) -- PHẦN MỚI --
        if player_rect.colliderect(enemy):
            # Kiểm tra xem có đang "Bất tử" không?
            if current_time - last_hit_time > invincible_duration:
                player_hp -= damage_per_hit
                last_hit_time = current_time # Ghi lại giờ bị đau
                print(f"Trúng đạn! HP: {player_hp}")
                
                # Hiệu ứng rung nhẹ hoặc xóa kẻ thù khi đâm vào (Tùy chọn)
                enemies.remove(enemy) 

    # --------------------
    # XỬ LÝ CHẾT & HỒI SINH
    # --------------------
    if player_hp <= 0:
        player_lives -= 1
        print(f"Mất 1 mạng! Còn: {player_lives}")
        
        if player_lives > 0:
            # Hồi sinh: Đầy máu, về vị trí cũ
            player_hp = player_max_hp
            player_x = WIDTH // 2 - player_width // 2
            player_y = HEIGHT - 70
            # Xóa hết kẻ thù trên màn hình để không bị chết oan ngay khi hồi sinh
            enemies.clear() 
            bullets.clear()
            pygame.time.delay(1000) # Dừng game 1 giây để thở
        else:
            print("GAME OVER")
            running = False # Thoát game (hoặc chuyển màn hình Game Over)

    # --------------------
    # DRAW (VẼ HÌNH)
    # --------------------
    
    # Hiệu ứng nhấp nháy khi bị thương (Bất tử)
    if current_time - last_hit_time < invincible_duration:
        # Nếu đang bất tử, cứ 5 frame thì vẽ, 5 frame thì ẩn -> Nhấp nháy
        if (current_time // 100) % 2 == 0:
            draw_player(player_x, player_y)
    else:
        # Bình thường vẽ liên tục
        draw_player(player_x, player_y)

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # --- VẼ UI (THANH MÁU & MẠNG) ---
    # Gọi hàm từ file health.py của bạn
    health.draw_health_bar(screen, 10, 10, player_hp, player_max_hp)
    health.draw_lives(screen, 10, 40, player_lives, font)
    
    # Vẽ điểm số (Dời sang bên phải một chút để không đè lên máu)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))
    # --------------------------------

    pygame.display.flip()

pygame.quit()