import pygame
import random
import math

# Colors for the explosion particles
FIRE_COLORS = [
    (255, 200, 0),  # bright yellow
    (255, 100, 0),  # orange
    (200, 0, 0)     # red
]

class Explosion:
    def __init__(self, x, y):
        """
        Creates a particle explosion at (x, y)
        """
        self.particles = []
        for _ in range(25):  # number of particles
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
        """
        Updates particle positions and reduces life
        """
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15  # gravity
            p["life"] -= 1
            p["radius"] = max(0, p["radius"] - 0.1)

        # Remove dead particles
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, surface):
        """
        Draws the particles on the given surface
        """
        for p in self.particles:
            life_ratio = p["life"] / p["max_life"]
            if life_ratio >= 0.66:
                color = FIRE_COLORS[0]
            elif life_ratio >= 0.33:
                color = FIRE_COLORS[1]
            else:
                color = FIRE_COLORS[2]

            pygame.draw.circle(surface, color, (int(p["x"]), int(p["y"])), int(p["radius"]))

    def is_dead(self):
        """
        Returns True if all particles are dead
        """
        return len(self.particles) == 0
