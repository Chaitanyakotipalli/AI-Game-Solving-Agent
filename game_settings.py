# game_settings.py

import pygame
from assets import load_assets

def game_settings():
    # Basic game settings
    agent_play = 1  # 1 for agent play, 0 for manual play
    total_duration = 60
    spawn_delay = 4000
    win_frame_index = 0
    win_animation_speed = 0.2

    # Load assets from assets.py (which already loads and scales all gifs)
    assets = load_assets()

    # Define global cooldown info for gun selection (in milliseconds)
    gun_cooldown_info = {
        'charizard': {'cooldown': 7500, 'last_placed': 0},
        'sniper':    {'cooldown': 5000, 'last_placed': 0},
        'cowboy':    {'cooldown': 5000, 'last_placed': 0},
        'samurai':   {'cooldown': 10000, 'last_placed': 0},
        'bomb':      {'cooldown': 15000, 'last_placed': 0}
    }

    # Define gun types and zombie types.
    # Note: These definitions assume that the corresponding scaled assets exist in the assets dictionary.
    gun_types = {
        "charizard": {
            "frames": assets["scaled_gun_frames"],
            "attack_frames": assets["scaled_gun_attack_frames"],
            "health": 4,
            "type": 0
        },
        "samurai": {
            "frames": assets["scaled_samurai_frames"],
            "attack_frames": assets["scaled_samurai_frames"],
            "health": 1,
            "speed": 4,
            "type": 1
        },
        "bomb": {
            "frames": assets["scaled_bomb_gif_frames"],
            "attack_frames": assets["scaled_bomb_gif_frames"],
            "health": 5,
            "type": 0
        },
        "cowboy": {
            "frames": assets["scaled_gunman1_still_frames"],
            "attack_frames": assets["scaled_gunman1_attack_frames"],
            "health": 4,
            "type": 1
        },
        "sniper": {
            "frames": assets["scaled_gunman2_still_frames"],
            "attack_frames": assets["scaled_gunman2_attack_frames"],
            "health": 4,
            "type": 1
        }
    }

    zombie_types = {
        "flying_zombie": {
            "frames": assets["scaled_zombie_flying_frames"],
            "attack_frames": assets["scaled_zombie_attack_frames"],
            "health": 3
        },
        "fast_zombie": {
            "frames": assets["scaled_zombie_fast_frames"],
            "attack_frames": assets["scaled_zombie_attack_frames"],
            "health": 3
        },
        "sheild_zombie": {
            "frames": assets["scaled_zombie_shield_frames"],
            "attack_frames": assets["scaled_zombie_attack_frames"],
            "health": 3,
            "speed": 1
        },
        "sports_zombie": {
            "frames": assets["scaled_zombie_sports_frames"],
            "attack_frames": assets["scaled_zombie_attack_frames"],
            "health": 3
        },
        "start_zombie": {
            "frames": assets["scaled_zombie_start_frames"],
            "attack_frames": assets["scaled_zombie_attack_frames"],
            "health": 3
        }
    }

    # Screen and grid settings
    screen_width, screen_height = 1500, 1200
    lawn_x, lawn_y = 270, 200
    lawn_width, lawn_height = 790, 800
    rows, cols = 5, 5
    row_height = lawn_height // rows
    col_width = lawn_width // cols

    # Preload fonts
    FONT_SMALL = pygame.font.Font(None, 70)
    FONT_LARGE = pygame.font.Font(None, 100)
    FONT_GAMEOVER = pygame.font.Font(None, 80)
    font = pygame.font.Font(None, 50)
    cooldown_font = pygame.font.Font(None, 50)

    # Load and scale background image
    background_image = pygame.image.load("background_night.jpg").convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Build the settings dictionary and merge with assets
    settings_dict = {
        "total_duration": total_duration,
        "win_frame_index": win_frame_index,
        "win_animation_speed": win_animation_speed,
        "agent_play": agent_play,
        "gun_cooldown_info": gun_cooldown_info,
        "gun_types": gun_types,
        "zombie_types": zombie_types,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "lawn_x": lawn_x,
        "lawn_y": lawn_y,
        "lawn_width": lawn_width,
        "lawn_height": lawn_height,
        "rows": rows,
        "cols": cols,
        "row_height": row_height,
        "col_width": col_width,
        "FONT_SMALL": FONT_SMALL,
        "FONT_LARGE": FONT_LARGE,
        "FONT_GAMEOVER": FONT_GAMEOVER,
        "font": font,
        "cooldown_font": cooldown_font,
        "background_image": background_image,
        "spawn_delay":spawn_delay,
    }

    # Merge assets dictionary into the settings dictionary
    settings_dict.update(assets)

    return settings_dict
