# assets.py

import pygame
from PIL import Image

from gif_paths import GIF_PATHS
# Assuming these constants are defined in your config file:
SCREEN_WIDTH,SCREEN_HEIGHT = 1500, 1200
lawn_x, lawn_y = 270, 200
lawn_width, lawn_height = 790, 800
rows, cols = 5, 5
ROW_HEIGHT = lawn_height // rows
COL_WIDTH = lawn_width // cols

def load_gif_frames(path):
    """Loads a GIF and returns a list of Pygame frames."""
    frames = []
    pil_image = Image.open(path)
    try:
        while True:
            frame = pil_image.convert("RGBA")
            mode, size, data = frame.mode, frame.size, frame.tobytes()
            py_frame = pygame.image.fromstring(data, size, mode)
            frames.append(py_frame)
            pil_image.seek(pil_image.tell() + 1)  # Move to next frame
    except EOFError:
        pass  # End of GIF reached
    return frames


def load_assets():
    # Load raw frames for each asset using paths from GIF_PATHS
    zombie_frames = load_gif_frames(GIF_PATHS["zombie"])
    zombie_attack_frames = load_gif_frames(GIF_PATHS["zombie_attack"])
    zombie_death_frames = load_gif_frames(GIF_PATHS["zombie_death"])
    zombie_dead_frames = load_gif_frames(GIF_PATHS["zombie_dead"])
    zombie_flying_frames = load_gif_frames(GIF_PATHS["zombie_flying"])
    zombie_fast_frames = load_gif_frames(GIF_PATHS["zombie_fast"])
    zombie_shield_frames = load_gif_frames(GIF_PATHS["zombie_shield"])
    zombie_sports_frames = load_gif_frames(GIF_PATHS["zombie_sports"])
    zombie_start_frames = load_gif_frames(GIF_PATHS["zombie_start"])
    
    gun_frames = load_gif_frames(GIF_PATHS["gun"])
    gun_attack_frames = load_gif_frames(GIF_PATHS["gun_attack"])
    
    samurai_frames = load_gif_frames(GIF_PATHS["samurai"])
    
    bomb_gif_frames = load_gif_frames(GIF_PATHS["bomb"])
    
    gunman1_still_frames = load_gif_frames(GIF_PATHS["gunman1"])
    gunman1_attack_frames = load_gif_frames(GIF_PATHS["gunman1_attack"])
    gunman2_still_frames = load_gif_frames(GIF_PATHS["gunman2"])
    gunman2_attack_frames = load_gif_frames(GIF_PATHS["gunman2_attack"])
    
    win_gif_frames = load_gif_frames(GIF_PATHS["win"])
    win_gif_2_frames = load_gif_frames(GIF_PATHS["win_2"])
    win_gif_3_frames = load_gif_frames(GIF_PATHS["win_3"])
    win_gif_start_frames = load_gif_frames(GIF_PATHS["win_start"])
    
    # Scale assets to fit grid sizes
    scaled_zombie_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_frames]
    scaled_zombie_attack_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_attack_frames]
    scaled_zombie_death_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_death_frames]
    scaled_zombie_dead_frames = [pygame.transform.scale(f, (COL_WIDTH * 2, ROW_HEIGHT * 2)) for f in zombie_dead_frames]
    scaled_zombie_flying_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_flying_frames]
    scaled_zombie_fast_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_fast_frames]
    scaled_zombie_shield_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_shield_frames]
    scaled_zombie_sports_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_sports_frames]
    scaled_zombie_start_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in zombie_start_frames]

    scaled_gun_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in gun_frames]
    scaled_gun_attack_frames = [pygame.transform.scale(f, (COL_WIDTH * 2, ROW_HEIGHT)) for f in gun_attack_frames]

    scaled_samurai_frames = [pygame.transform.scale(f, (int(COL_WIDTH * 1.5), int(ROW_HEIGHT * 1.5))) for f in samurai_frames]

    scaled_bomb_gif_frames = [pygame.transform.scale(f, (int(COL_WIDTH * 0.5), int(ROW_HEIGHT * 0.7))) for f in bomb_gif_frames]

    scaled_gunman1_still_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in gunman1_still_frames]
    scaled_gunman1_attack_frames = [pygame.transform.scale(f, (COL_WIDTH * 2, ROW_HEIGHT)) for f in gunman1_attack_frames]

    scaled_gunman2_still_frames = [pygame.transform.scale(f, (COL_WIDTH, ROW_HEIGHT)) for f in gunman2_still_frames]
    scaled_gunman2_attack_frames = [pygame.transform.scale(f, (COL_WIDTH * 2, ROW_HEIGHT)) for f in gunman2_attack_frames]

    scaled_win_gif_frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in win_gif_frames]
    scaled_win_gif2_frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in win_gif_2_frames]
    scaled_win_gif3_frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in win_gif_3_frames]
    scaled_win_gif_starting_frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in win_gif_start_frames]

    return {
        "scaled_zombie_frames": scaled_zombie_frames,
        "scaled_zombie_attack_frames": scaled_zombie_attack_frames,
        "scaled_zombie_death_frames": scaled_zombie_death_frames,
        "scaled_zombie_dead_frames": scaled_zombie_dead_frames,
        "scaled_zombie_flying_frames": scaled_zombie_flying_frames,
        "scaled_zombie_fast_frames": scaled_zombie_fast_frames,
        "scaled_zombie_shield_frames": scaled_zombie_shield_frames,
        "scaled_zombie_sports_frames": scaled_zombie_sports_frames,
        "scaled_zombie_start_frames": scaled_zombie_start_frames,
        "scaled_gun_frames": scaled_gun_frames,
        "scaled_gun_attack_frames": scaled_gun_attack_frames,
        "scaled_samurai_frames": scaled_samurai_frames,
        "scaled_bomb_gif_frames": scaled_bomb_gif_frames,
        "scaled_gunman1_still_frames": scaled_gunman1_still_frames,
        "scaled_gunman1_attack_frames": scaled_gunman1_attack_frames,
        "scaled_gunman2_still_frames": scaled_gunman2_still_frames,
        "scaled_gunman2_attack_frames": scaled_gunman2_attack_frames,
        "scaled_win_gif_frames": scaled_win_gif_frames,
        "scaled_win_gif2_frames": scaled_win_gif2_frames,
        "scaled_win_gif3_frames": scaled_win_gif3_frames,
        "scaled_win_gif_starting_frames": scaled_win_gif_starting_frames,
        # Optionally, you can also return the raw frames if needed
        "zombie_frames": zombie_frames,
        "zombie_attack_frames": zombie_attack_frames,
        "zombie_death_frames": zombie_death_frames,
        "zombie_dead_frames": zombie_dead_frames,
        "zombie_flying_frames": zombie_flying_frames,
        "zombie_fast_frames": zombie_fast_frames,
        "zombie_shield_frames": zombie_shield_frames,
        "zombie_sports_frames": zombie_sports_frames,
        "zombie_start_frames": zombie_start_frames,
        "gun_frames": gun_frames,
        "gun_attack_frames": gun_attack_frames,
        "samurai_frames": samurai_frames,
        "bomb_gif_frames": bomb_gif_frames,
        "gunman1_still_frames": gunman1_still_frames,
        "gunman1_attack_frames": gunman1_attack_frames,
        "gunman2_still_frames": gunman2_still_frames,
        "gunman2_attack_frames": gunman2_attack_frames,
        "win_gif_frames": win_gif_frames,
        "win_gif_2_frames": win_gif_2_frames,
        "win_gif_3_frames": win_gif_3_frames,
        "win_gif_start_frames": win_gif_start_frames,
    }
