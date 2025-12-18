import pygame
import os

class Background:
    def __init__(self, image_name, width, height):
        # Get absolute path to the image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, ".."))
        image_path = os.path.join(project_root, "background", image_name)

        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Cannot find background image at: {image_path}")

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
# 