import pygame
import os

pygame.mixer.init()

BASE_PATH = os.path.dirname(__file__)
SOUND_PATH = os.path.join(BASE_PATH, "sounds")

shoot = pygame.mixer.Sound(os.path.join(SOUND_PATH, "shoot.mp3"))
explosion = pygame.mixer.Sound(os.path.join(SOUND_PATH, "explosion.mp3"))
game_over = pygame.mixer.Sound(os.path.join(SOUND_PATH, "gameover.mp3"))

def play_shoot():
    shoot.play()

def play_explosion():
    explosion.play()

def play_game_over():
    game_over.play()