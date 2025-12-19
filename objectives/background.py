import pygame
import os
import random


class Background:
    """Parallax background with a base image and multiple moving star layers.

    If only one background image exists, the class will draw it scaled and
    render two procedural star layers on top that scroll at different speeds
    to produce a parallax effect.
    """

    def __init__(self, image_name, width, height):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, ".."))
        image_path = os.path.join(project_root, "background", image_name)

        self.width = width
        self.height = height

        self.base = None
        if os.path.isfile(image_path):
            try:
                img = pygame.image.load(image_path).convert()
                self.base = pygame.transform.scale(img, (width, height))
            except Exception:
                self.base = None

        # Create two star layers (far and near) as surfaces with random points
        self.layers = []
        # Layer: (surface, speed_y, offset_y)
        # Far layer: slow, sparse, dim
        self.layers.append(self._make_star_layer(width, height, density=0.0008, color=(120, 180, 255), alpha=90, speed=0.2))
        # Near layer: faster, denser, brighter
        self.layers.append(self._make_star_layer(width, height, density=0.0022, color=(200, 220, 255), alpha=140, speed=0.6))

    def _make_star_layer(self, w, h, density=0.001, color=(255, 255, 255), alpha=150, speed=0.5):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        num_stars = max(8, int(w * h * density))
        for i in range(num_stars):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            size = random.choice((1, 1, 2))
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            s.fill((*color, alpha))
            surf.blit(s, (x, y))
        return {"surf": surf, "speed": speed, "offset": 0}

    def update(self):
        # advance each layer offset
        for layer in self.layers:
            layer["offset"] += layer["speed"]
            # wrap offset
            if layer["offset"] >= self.height:
                layer["offset"] -= self.height

    def draw(self, screen):
        # Draw base image if present, otherwise fill with dark gradient
        if self.base:
            screen.blit(self.base, (0, 0))
        else:
            screen.fill((5, 5, 12))

        # Draw star layers with vertical tiling to fill screen
        for layer in self.layers:
            off = int(layer["offset"]) % self.height
            surf = layer["surf"]
            # Draw main copy
            screen.blit(surf, (0, off))
            # Draw second copy above/below to tile
            screen.blit(surf, (0, off - self.height))

# 