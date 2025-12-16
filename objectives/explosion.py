import pygame
import random
import math

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
FIRE_COLORS = [(255, 200, 50), (255, 140, 0), (255, 60, 0)]  # yellow → orange → red

# --------------------
# PLAYER
# --------------------
player_width, player_height = 50, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 70
player_speed = 6

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

# --------------------
# EXPLOSIONS
# --------------------
explosions = []

class Explosion:
    def __init__(self, x, y):
        self.particles = []
        for _ in range(25):  # more particles for bigger explosion
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            life = random.randint(20, 40)
            self.particles.append({
                "x": x,
                "y": y,
                "vx": speed * math.cos(angle),
                "vy": speed * math.sin(angle),
                "life": life,
                "max_life": life,
                "radius": random.randint(3, 6)
            })

    def update(self):
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15  # gravity pulls particles down
            p["life"] -= 1
            p["radius"] = max(0, p["radius"] - 0.1)
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, surface):
        for p in self.particles:
            life_ratio = p["life"] / p["max_life"]
            if life_ratio > 0.66:
                color = FIRE_COLORS[0]
            elif life_ratio > 0.33:
                color = FIRE_COLORS[1]
            else:
                color = FIRE_COLORS[2]
            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), int(p["radius"]))

    def is_dead(self):
        return len(self.particles) == 0

# --------------------
# FUNCTIONS
# --------------------
def draw_player(x, y):
    pygame.draw.polygon(
        screen,
        WHITE,
        [(x, y + player_height), (x + player_width // 2, y), (x + player_width, y + player_height)]
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
    screen.fill(BLACK)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x + player_width // 2 - 3, player_y, 6, 12))

    # PLAYER INPUT
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

    # ENEMY UPDATE & COLLISIONS
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

        # Collision with bullets
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                explosions.append(Explosion(enemy.centerx, enemy.centery))  # trigger fire explosion
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

    # UPDATE EXPLOSIONS
    for exp in explosions[:]:
        exp.update()
        if exp.is_dead():
            explosions.remove(exp)

    # DRAW EVERYTHING
    draw_player(player_x, player_y)

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    for exp in explosions:
        exp.draw(screen)

    draw_score()
    pygame.display.flip()

pygame.quit()
