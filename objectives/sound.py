import pygame
import os

# --------------------
# PATHS
# --------------------
BASE_PATH = os.path.dirname(__file__)
SOUND_PATH = os.path.join(BASE_PATH, "sounds")

# --------------------
# SOUND VARIABLES
# --------------------
shoot = None
explosion = None
game_over = None
victory = None
current_volume = 0.5  # Default Volume (50%)


# --------------------
# INIT SOUND
# --------------------
def init_sound():
    global shoot, explosion, game_over, victory

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # Load Sound Effects (use error handling just in case)
    try:
        shoot = pygame.mixer.Sound(os.path.join(SOUND_PATH, "shoot.mp3"))
        explosion = pygame.mixer.Sound(os.path.join(SOUND_PATH, "explosion.mp3"))
        game_over = pygame.mixer.Sound(os.path.join(SOUND_PATH, "game_over.mp3"))
        # Optional victory sound (may not exist in repo)
        try:
            victory = pygame.mixer.Sound(os.path.join(SOUND_PATH, "victory.mp3"))
            victory.set_volume(0.6)
        except Exception:
            victory = None

        # Set SFX volumes
        if shoot: shoot.set_volume(0.3)
        if explosion: explosion.set_volume(0.3)
    except FileNotFoundError:
        print("Warning: Sound files not found.")


# --------------------
# SOUND FUNCTIONS
# --------------------
def play_shoot():
    if shoot: shoot.play()


def play_explosion():
    if explosion: explosion.play()


def play_game_over():
    if game_over: game_over.play()


def play_victory():
    if victory: victory.play()


def play_background_music():
    try:
        pygame.mixer.music.load(os.path.join(SOUND_PATH, "background_music.mp3"))
        pygame.mixer.music.set_volume(current_volume)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Warning: Background music not found.")


def stop_background_music():
    try:
        pygame.mixer.music.fadeout(1000)
    except Exception:
        pass


def set_music_volume(vol):
    global current_volume
    current_volume = max(0.0, min(1.0, vol))
    try:
        pygame.mixer.music.set_volume(current_volume)
    except Exception:
        pass