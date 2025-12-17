import pygame
import os

# --------------------
# PATHS
# --------------------
BASE_PATH = os.path.dirname(__file__)
SOUND_PATH = os.path.join(BASE_PATH, "sounds")

# --------------------
# SOUND VARIABLES (will be initialized later)
# --------------------
shoot = None
explosion = None
game_over = None

# --------------------
# INIT SOUND
# --------------------
def init_sound():
    global shoot, explosion, game_over

    # Make sure mixer is initialized
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    shoot = pygame.mixer.Sound(os.path.join(SOUND_PATH, "shoot.mp3"))
    explosion = pygame.mixer.Sound(os.path.join(SOUND_PATH, "explosion.mp3"))
    game_over = pygame.mixer.Sound(os.path.join(SOUND_PATH, "game_over.mp3"))

# --------------------
# SOUND FUNCTIONS
# --------------------
def play_shoot():
    if shoot:
        shoot.play()

def play_explosion():
    if explosion:
        explosion.play()

def play_game_over():
    if game_over:
        game_over.play()

def play_background_music():
    pygame.mixer.music.load(os.path.join(SOUND_PATH, "background_music.mp3"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

def stop_background_music():
    pygame.mixer.music.fadeout(1000)
