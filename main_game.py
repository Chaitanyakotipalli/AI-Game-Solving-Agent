import pygame
import sys
import random
from game_settings import game_settings

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1500, 1200))
# Get settings and assets from game_settings.py
settings = game_settings()

# Unpack settings
screen_width = settings["screen_width"]
screen_height = settings["screen_height"]
background_image = settings["background_image"]
total_duration = settings["total_duration"]
win_frame_index = settings["win_frame_index"]
win_animation_speed = settings["win_animation_speed"]
agent_play = settings["agent_play"]

gun_cooldown_info = settings["gun_cooldown_info"]  # global cooldown info for guns
gun_types = settings["gun_types"]
zombie_types = settings["zombie_types"]

lawn_x = settings["lawn_x"]
lawn_y = settings["lawn_y"]
lawn_width = settings["lawn_width"]
lawn_height = settings["lawn_height"]
rows = settings["rows"]
cols = settings["cols"]
row_height = settings["row_height"]
col_width = settings["col_width"]

FONT_SMALL = settings["FONT_SMALL"]
FONT_LARGE = settings["FONT_LARGE"]
FONT_GAMEOVER = settings["FONT_GAMEOVER"]
font = settings["font"]
cooldown_font = settings["cooldown_font"]

scaled_win_gif_frames = settings["scaled_win_gif_frames"]
scaled_win_gif3_frames = settings["scaled_win_gif3_frames"]
# Get the start_game gif frames from settings (assuming it exists, otherwise add to game_settings.py)
start_game_frames = settings.get("start_game_frames", [])  # Fallback to empty list if not found

# Create game window and clock
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Plants vs. Zombies Clone")
clock = pygame.time.Clock()

# ---------------------------------------------------------------------------
# Create Gun Icons for the Selection Bar
# ---------------------------------------------------------------------------
gun_icon_size = (100, 100)
gun_icons = {}
for gun_name, gun_data in gun_types.items():
    # Assuming each gun's "frames" list is non-empty
    icon_image = pygame.transform.scale(gun_data["frames"][0], gun_icon_size)
    gun_icons[gun_name] = icon_image

selection_bar_height = (gun_icon_size[1] + 10) * len(gun_types) + 10  
selection_bar_rect = pygame.Rect(20, (screen_height - selection_bar_height) // 2, 140, selection_bar_height)
selected_gun_type = None

# ---------------------------------------------------------------------------
# CLASS DEFINITIONS
# ---------------------------------------------------------------------------
class Zombie:
    def __init__(self, x, y, zombie_type):
        self.x = x
        self.y = y
        self.type = zombie_type
        self.frames = zombie_types[zombie_type]["frames"]
        self.attack_frames = zombie_types[zombie_type].get("attack_frames", self.frames)
        self.health = zombie_types[zombie_type]["health"]
        self.speed = zombie_types[zombie_type].get("speed", 1)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.state = "moving"
        self.attack_timer = 0
        self.attack_interval = 1000
        self.dead = False
        self.finished = False
        self.target = None

    def update(self, dt, guns):
        if self.dead:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.finished = True
            return

        if self.state == "moving":
            self.x -= self.speed
            for gun in guns:
                if abs(self.x - gun.x) < col_width and self.y == gun.y:
                    self.state = "attacking"
                    self.frames = self.attack_frames
                    self.target = gun
                    break
        elif self.state == "attacking":
            self.attack_timer += dt
            if self.attack_timer >= self.attack_interval:
                self.attack_timer = 0
                if self.target and self.target.alive:
                    self.target.health -= 1
                    if self.target.health <= 0:
                        self.target.alive = False
                        self.state = "moving"
                        self.frames = zombie_types[self.type]["frames"]
                        self.target = None

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

    def draw(self, surface):
        current_frame = self.frames[int(self.frame_index) % len(self.frames)]
        surface.blit(current_frame, (self.x, self.y))

class Gun:
    def __init__(self, x, y, gun_data):
        self.x = x
        self.y = y
        self.frames = gun_data["frames"]
        self.attack_frames = gun_data.get("attack_frames", None)
        self.health = gun_data["health"]
        self.type1 = gun_data["type"]
        self.is_samurai = ("speed" in gun_data)
        self.speed = gun_data.get("speed", 0)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.state = "idle"
        self.attack_timer = 0
        self.attack_interval = 2000
        self.alive = True
        self.target = None
        if self.is_samurai:
            self.state = "charging"
            self.collision_time = None

    def update(self, dt, zombies):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        if not self.is_samurai:
            if self.state == "idle":
                for z in zombies:
                    if abs(z.x - self.x) < col_width and z.y == self.y and not z.dead:
                        self.state = "attacking"
                        self.target = z
                        break
            elif self.state == "attacking":
                self.attack_timer += dt
                if self.attack_timer >= self.attack_interval:
                    self.attack_timer = 0
                    if self.target and not self.target.dead:
                        self.target.health -= 1
                        if self.target.health <= 0:
                            self.target.dead = True
                            # Adjust target death animation based on gun type
                            if self.type1 == 0:
                                self.target.frames = settings.get("scaled_zombie_death_frames", self.target.frames)
                            else:
                                self.target.frames = settings.get("scaled_zombie_dead_frames", self.target.frames)
                            self.target.frame_index = 0
                            self.state = "idle"
                            self.target = None
            if self.health <= 0:
                self.alive = False
        else:
            # Samurai logic
            if self.state == "charging":
                self.x += self.speed
                samurai_width = gun_types["samurai"]["frames"][0].get_width()
                samurai_height = gun_types["samurai"]["frames"][0].get_height()
                samurai_rect = pygame.Rect(self.x, self.y, samurai_width, samurai_height)
                for z in zombies:
                    zombie_rect = pygame.Rect(z.x, z.y, col_width, row_height)
                    if samurai_rect.colliderect(zombie_rect) and not z.dead:
                        if self.collision_time is None:
                            self.collision_time = pygame.time.get_ticks()
                            self.frames = gun_types["samurai"]["frames"]
                            z.dead = True
                            z.frames = settings.get("scaled_zombie_dead_frames", z.frames)
                            z.frame_index = 0
                            z.state = "dead"
                        else:
                            self.alive = False
                        break
                if self.x > screen_width:
                    self.alive = False

    def draw(self, surface):
        frames_used = self.attack_frames if (self.state != "idle" and self.attack_frames) else self.frames
        current_frame = frames_used[int(self.frame_index) % len(frames_used)]
        surface.blit(current_frame, (self.x, self.y))

class Bomb:
    def __init__(self, x, y, explosion_radius=150, damage=999, timer=4800):
        self.x = x
        self.y = y
        self.explosion_radius = explosion_radius
        self.damage = damage
        self.timer = timer
        self.placed_time = pygame.time.get_ticks()
        self.alive = True
        self.exploded = False
        self.frames = settings.get("scaled_bomb_gif_frames")
        self.frame_index = 0
        self.animation_speed = 0.15
        self.explosion_display_duration = 1000
        self.explosion_start_time = None

    def update(self, zombies):
        current_time = pygame.time.get_ticks()
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        if not self.exploded and (current_time - self.placed_time >= self.timer):
            self.explode(zombies)
            self.explosion_start_time = current_time

        if self.exploded and (current_time - self.explosion_start_time >= self.explosion_display_duration):
            self.alive = False

    def explode(self, zombies):
        self.exploded = True
        for z in zombies[:]:
            if abs(z.x - self.x) <= self.explosion_radius and abs(z.y - self.y) <= self.explosion_radius:
                z.health -= self.damage
                if z.health <= 0:
                    z.dead = True
                    zombies.remove(z)

    def draw(self, surface):
        current_frame = self.frames[int(self.frame_index) % len(self.frames)]
        surface.blit(current_frame, (self.x, self.y))

# ---------------------------------------------------------------------------
# DRAW SELECTION BAR FUNCTION
# ---------------------------------------------------------------------------
def draw_selection_bar(surface, font):
    bar_surface = pygame.Surface((selection_bar_rect.width, selection_bar_rect.height))
    bar_surface.set_alpha(150)
    bar_surface.fill((20, 20, 20))
    surface.blit(bar_surface, (selection_bar_rect.left, selection_bar_rect.top))
    
    current_time = pygame.time.get_ticks()
    y_offset = selection_bar_rect.top + 10
    for name, icon in gun_icons.items():
        icon_rect = pygame.Rect(selection_bar_rect.left + 20, y_offset, gun_icon_size[0], gun_icon_size[1])
        surface.blit(icon, icon_rect)
        if selected_gun_type == name:
            pygame.draw.rect(surface, (0, 255, 0), icon_rect, 3)
        if name in gun_cooldown_info:
            cooldown_time = gun_cooldown_info[name]['cooldown']
            last_placed = gun_cooldown_info[name]['last_placed']
            time_left = max(0, (cooldown_time - (current_time - last_placed)) / 1000)
            if time_left > 0:
                cooldown_text = font.render(f"{int(time_left)}s", True, (255, 255, 0))
                surface.blit(cooldown_text, (icon_rect.right + 15, y_offset + 20))
        y_offset += gun_icon_size[1] + 10

# ---------------------------------------------------------------------------
# TIMER AND SCORE RENDERING FUNCTION
# ---------------------------------------------------------------------------
def render_timer():
    elapsed_sec = (pygame.time.get_ticks() - start_time) // 1000
    remaining_time = max(total_duration - elapsed_sec, 0)
    timer_text = FONT_SMALL.render(f"Time Left: {remaining_time}s", True, (255, 255, 0))
    timer_rect = timer_text.get_rect(center=(screen_width - 200, screen_height - 1000))
    bg_surface = pygame.Surface((timer_rect.width + 20, timer_rect.height + 20))
    bg_surface.set_alpha(150)
    bg_surface.fill((0, 0, 0))
    bg_rect = bg_surface.get_rect(center=(screen_width - 200, screen_height - 1000))
    screen.blit(bg_surface, bg_rect)
    screen.blit(timer_text, timer_rect)
    return remaining_time

def render_score(zombie_kill_count):
    score_text = FONT_SMALL.render(f"Score: {zombie_kill_count}", True, (255, 255, 0))
    score_rect = score_text.get_rect(center=(screen_width - 1200, screen_height - 1000))  # Adjusted position

    # Background rectangle for better visibility
    bg_surface = pygame.Surface((score_rect.width + 20, score_rect.height + 10))
    bg_surface.set_alpha(150)  # Semi-transparent background
    bg_surface.fill((0, 0, 0))
    bg_rect = bg_surface.get_rect(center=(screen_width - 1200, screen_height - 1000))

    screen.blit(bg_surface, bg_rect)
    screen.blit(score_text, score_rect)

# ---------------------------------------------------------------------------
# UTILITY: GET AVAILABLE GUN TYPE
# ---------------------------------------------------------------------------
def get_available_gun_type(preferred_type=None):
    current_time = pygame.time.get_ticks()
    if preferred_type:
        info = gun_cooldown_info.get(preferred_type)
        if info and current_time - info['last_placed'] >= info['cooldown']:
            return preferred_type
    for gun in ['charizard', 'sniper', 'cowboy']:
        info = gun_cooldown_info.get(gun)
        if info and current_time - info['last_placed'] >= info['cooldown']:
            return gun
    return None

# ---------------------------------------------------------------------------
# BOMB PLACEMENT SCORING AND ATTEMPT FUNCTION
# ---------------------------------------------------------------------------
def compute_bomb_score(row, zombies):
    zombies_in_row = [z for z in zombies if 0 <= (z.y - lawn_y) // row_height == row]
    if not zombies_in_row:
        return 0, None
    Z = len(zombies_in_row)
    immediate_positions = []
    if Z >= 2:
        for i in range(len(zombies_in_row)):
            for j in range(i+1, len(zombies_in_row)):
                if abs(zombies_in_row[i].x - zombies_in_row[j].x) < 2 * col_width:
                    immediate_positions.append(zombies_in_row[i].x)
                    immediate_positions.append(zombies_in_row[j].x)
        if immediate_positions:
            min_x = min(immediate_positions)
            col_index = int((min_x - lawn_x) // col_width)
            bomb_col = max(col_index - 1, 0)
            return 1000, (row, bomb_col)
    cell_center_x = lawn_x + col_width / 2
    avg_distance = sum(z.x - cell_center_x for z in zombies_in_row) / Z
    proximity = 1 - min(max(avg_distance / lawn_width, 0), 1)
    current_time = pygame.time.get_ticks()
    bomb_info = gun_cooldown_info.get('bomb', {'last_placed': 0, 'cooldown': 10000})
    cd_penalty = 100 if current_time - bomb_info['last_placed'] < bomb_info['cooldown'] else 0
    group_count = 0
    for i in range(len(zombies_in_row)):
        for j in range(i+1, len(zombies_in_row)):
            if abs(zombies_in_row[i].x - zombies_in_row[j].x) < col_width:
                group_count += 1
    alpha, gamma, delta = 10, 10, 20
    score = alpha * Z + gamma * proximity + delta * group_count - cd_penalty
    return score, (row, 0)

def attempt_bomb_placement(zombies, bombs, guns):
    current_time = pygame.time.get_ticks()
    best_row = None
    best_score = -float('inf')
    best_pos = None
    for row in range(rows):
        score, pos = compute_bomb_score(row, zombies)
        if score > best_score:
            best_score = score
            best_row = row
            best_pos = pos
    threshold = 50
    if best_row is not None and best_score >= threshold and best_pos is not None:
        row_index, col_index = best_pos
        empty_col = None
        for offset in range(cols):
            left_col = col_index - offset if col_index - offset >= 0 else None
            right_col = col_index + offset if col_index + offset < cols else None
            if left_col is not None:
                bomb_x = lawn_x + left_col * col_width
                bomb_y = lawn_y + row_index * row_height
                if not any((b.x == bomb_x and b.y == bomb_y) for b in bombs) and not any((g.x == bomb_x and g.y == bomb_y) for g in guns):
                    empty_col = left_col
                    break
            if right_col is not None:
                bomb_x = lawn_x + right_col * col_width
                bomb_y = lawn_y + row_index * row_height
                if not any((b.x == bomb_x and b.y == bomb_y) for b in bombs) and not any((g.x == bomb_x and g.y == bomb_y) for g in guns):
                    empty_col = right_col
                    break
        if empty_col is not None:
            bomb_x = lawn_x + empty_col * col_width
            bomb_y = lawn_y + row_index * row_height
            if current_time - gun_cooldown_info['bomb']['last_placed'] >= gun_cooldown_info['bomb']['cooldown']:
                bombs.append(Bomb(bomb_x, bomb_y))
                gun_cooldown_info['bomb']['last_placed'] = current_time
                print(f"Bomb placed in row {best_row} at col {empty_col} with score {best_score:.2f}.")
            else:
                print("Bomb is on cooldown; cannot place now.")
        else:
            print("No empty spot found in the row; cannot place bomb.")

# ---------------------------------------------------------------------------
# AGENT LOGIC
# ---------------------------------------------------------------------------
class DefenseAgent:
    def __init__(self, placement_interval=3000):
        self.placement_interval = placement_interval
        self.last_update = pygame.time.get_ticks()
        self.prev_zombie_counts = {row: 0 for row in range(rows)}

    def update(self, zombies, guns, bombs):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.placement_interval:
            attempt_bomb_placement(zombies, bombs, guns)
            self.maintain_defense(zombies, guns, bombs)
            self.last_update = current_time

    def find_available_spots_in_row(self, row, guns):
        occupied_columns = {(g.x - lawn_x) // col_width for g in guns if (g.y - lawn_y) // row_height == row}
        return [col for col in range(cols) if col not in occupied_columns]

    def evaluate_threat(self, row, zombies, current_gun_count):
        zombies_in_row = [z for z in zombies if 0 <= (z.y - lawn_y) // row_height == row]
        count = len(zombies_in_row)
        if count == 0:
            return 0
        closest_zombie_x = min(z.x for z in zombies_in_row)
        distance_factor = max(0, (lawn_x + lawn_width - closest_zombie_x) / lawn_width)
        alpha, beta, gamma = 1.0, 2.0, 1.0
        threat = alpha * count + beta * (1 - distance_factor) - gamma * current_gun_count
        return threat

    def check_leftmost_defense(self, row, guns):
        for g in guns:
            if (g.y - lawn_y) // row_height == row and (g.x - lawn_x) // col_width == 0:
                return False
        return True

    def maintain_defense(self, zombies, guns, bombs):
        guns[:] = [g for g in guns if getattr(g, "alive", True)]
        current_time = pygame.time.get_ticks()
        for row in range(rows):
            zombies_in_row = [z for z in zombies if 0 <= (z.y - lawn_y) // row_height == row]
            current_zombie_count = len(zombies_in_row)
            current_gun_count = len([g for g in guns if 0 <= (g.y - lawn_y) // row_height == row])
            if current_zombie_count == 0:
                continue
            closest_zombie_x = min(z.x for z in zombies_in_row)
            emergency_threshold = 2 * col_width
            left_defense_missing = self.check_leftmost_defense(row, guns)
            emergency_condition = ((closest_zombie_x - lawn_x) <= emergency_threshold or left_defense_missing) and (current_gun_count < current_zombie_count)
            attempt_bomb_placement(zombies, bombs, guns)
            if emergency_condition:
                gun_to_place = get_available_gun_type(preferred_type="samurai")
                if gun_to_place is None:
                    gun_to_place = get_available_gun_type()
                if gun_to_place is not None:
                    available_spots = self.find_available_spots_in_row(row, guns)
                    if available_spots:
                        col = available_spots[0]
                        gun_x = lawn_x + col * col_width
                        gun_y = lawn_y + row * row_height
                        new_gun = Gun(gun_x, gun_y, gun_types[gun_to_place])
                        guns.append(new_gun)
                        gun_cooldown_info[gun_to_place]['last_placed'] = current_time
                        print(f"Emergency: Placed {gun_to_place} at ({gun_x}, {gun_y}) in row {row}.")
                self.prev_zombie_counts[row] = current_zombie_count
                continue
            threat = self.evaluate_threat(row, zombies, current_gun_count)
            threat_threshold = 1.5
            if threat > threat_threshold and current_gun_count < current_zombie_count:
                available_spots = self.find_available_spots_in_row(row, guns)
                if available_spots:
                    col = available_spots[0]
                    gun_x = lawn_x + col * col_width
                    gun_y = lawn_y + row * row_height
                    selected_gun_type = get_available_gun_type()
                    if selected_gun_type is not None:
                        new_gun = Gun(gun_x, gun_y, gun_types[selected_gun_type])
                        guns.append(new_gun)
                        gun_cooldown_info[selected_gun_type]['last_placed'] = current_time
                        print(f"Placed {selected_gun_type} at ({gun_x}, {gun_y}) in row {row} (Threat: {threat:.2f}).")
            self.prev_zombie_counts[row] = current_zombie_count

# ---------------------------------------------------------------------------
# MAIN GAME LOOP AND AGENT LOGIC
# ---------------------------------------------------------------------------
def main():
    global selected_gun_type, start_time
    zombies = []
    guns = []
    bombs = []
    spawn_timer = 0
    spawn_delay =settings["spawn_delay"] # spawn a zombie every 4 seconds (fixed typo from original code)
    y_pos_array = [lawn_y + row_height * i for i in range(rows)]
    game_over = False
    win = False
    global total_duration
    
    # New variables for start game animation
    showing_start_animation = True
    start_animation_duration = 2000  # 2 seconds
    start_animation_frame_index = 0
    start_animation_speed = 0.15
    
    # Zombie kill counter
    zombie_kill_count = 0
    
    # We'll set the start time after the start animation finishes
    real_start_time = pygame.time.get_ticks()
    start_time = real_start_time  # This will be updated once the animation is done
    
    win_frame_index = settings["win_frame_index"]
    win_animation_speed = settings["win_animation_speed"]
    time_stop = True
    agent = DefenseAgent(placement_interval=1000)
    running = True
    
    while running:
        dt = clock.tick(60)
        spawn_multiplier = 1
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not showing_start_animation and not agent_play and not game_over and not win and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if selection_bar_rect.collidepoint(mouse_x, mouse_y):
                    relative_y = mouse_y - selection_bar_rect.top
                    index = relative_y // (gun_icon_size[1] + 10)
                    keys = list(gun_types.keys())
                    if 0 <= index < len(keys):
                        selected_gun_type = keys[index]
                elif (lawn_x <= mouse_x < lawn_x + lawn_width and
                      lawn_y <= mouse_y < lawn_y + lawn_height):
                    grid_col = (mouse_x - lawn_x) // col_width
                    grid_row = (mouse_y - lawn_y) // row_height
                    gun_x = lawn_x + grid_col * col_width
                    gun_y = lawn_y + grid_row * row_height
                    if selected_gun_type == "bomb":
                        if current_time - gun_cooldown_info.get("bomb", {'last_placed':0})['last_placed'] >= 10000:
                            bombs.append(Bomb(gun_x, gun_y))
                            gun_cooldown_info["bomb"]['last_placed'] = current_time
                        else:
                            print("Bomb is still on cooldown!")
                    elif selected_gun_type is not None:
                        if current_time - gun_cooldown_info.get(selected_gun_type, {'last_placed':0})['last_placed'] >= 10000:
                            guns.append(Gun(gun_x, gun_y, gun_types[selected_gun_type]))
                            gun_cooldown_info[selected_gun_type]['last_placed'] = current_time
                        else:
                            print(f"{selected_gun_type} is still on cooldown!")
                    selected_gun_type = None

        # Handle start game animation
        if showing_start_animation:
            if current_time - real_start_time >= start_animation_duration:
                showing_start_animation = False
                start_time = pygame.time.get_ticks()  # Set actual game start time after animation
            else:
                # Draw start animation
                screen.blit(background_image, (0, 0))
                
                if start_game_frames and len(start_game_frames) > 0:
                    start_animation_frame_index += start_animation_speed
                    if start_animation_frame_index >= len(start_game_frames):
                        start_animation_frame_index = 0
                    
                    current_frame = start_game_frames[int(start_animation_frame_index) % len(start_game_frames)]
                    frame_rect = current_frame.get_rect(center=(screen_width // 2, screen_height // 2))
                    screen.blit(current_frame, frame_rect)
                else:
                    # Fallback if no frames are available
                    start_text = FONT_LARGE.render("STARTING GAME...", True, (255, 255, 0))
                    start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
                    screen.blit(start_text, start_text_rect)
                
                pygame.display.flip()
                continue  # Skip the rest of the game loop

        if agent_play and not game_over and not win:
            agent.update(zombies, guns, bombs)

        if not game_over and not win and (current_time - start_time >= total_duration * 1000):
            win = True

        remaining_time = render_timer()
        if remaining_time <= total_duration and remaining_time >= total_duration*(0.6):
            spawn_multiplier = 1
        elif remaining_time <= total_duration*(0.6) and remaining_time >= total_duration*(0.3):
            spawn_multiplier = 2
        elif remaining_time <= total_duration*(0.3) and remaining_time >= 0:
            spawn_multiplier = 3

        if not game_over and not win:
            spawn_timer += dt
            if spawn_timer >= spawn_delay:
                spawn_timer = 0
                for _ in range(spawn_multiplier):
                    zombie_type = random.choice(list(zombie_types.keys()))
                    zombie_y = random.choice(y_pos_array)
                    zombies.append(Zombie(screen_width, zombie_y, zombie_type))
                    
            prev_zombie_count = len(zombies)  # Total zombies before update

            # Update zombies
            for z in zombies[:]:
                z.update(dt, guns)
                if z.x < lawn_x and not z.dead:
                    game_over = True
                    break

            # Remove zombies that are dead and finished
            zombies = [z for z in zombies if not (z.dead and z.finished)]

            # Count remaining zombies
            current_zombie_count = len(zombies)

            # Calculate new kills
            new_kills = prev_zombie_count - current_zombie_count
            if new_kills > 0:
                zombie_kill_count += new_kills

            
            for g in guns:
                g.update(dt, zombies)
            guns = [g for g in guns if g.alive]
            for b in bombs:
                b.update(zombies)
            bombs = [b for b in bombs if b.alive]
            zombies = [z for z in zombies if not (z.dead and z.finished)]

        screen.blit(background_image, (0, 0))
        draw_selection_bar(screen, cooldown_font)
        render_score(zombie_kill_count)
        if time_stop:
            remaining_time = render_timer()
            
                # Display the zombie kill counter
        

        if not win and not game_over:
            # Update and draw zombies
            for z in zombies:
                z.draw(screen)

            # Update and draw guns
            for g in guns:
                g.draw(screen)

            # Update and draw bombs
            for b in bombs:
                b.draw(screen)

        elif win:
            # Handle win animation
            screen.blit(background_image, (0, 0))
            
            # Always display the win text
            win_text = FONT_GAMEOVER.render("YOU WIN!", True, (0, 255, 0))
            win_text_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 4))  # Position at top quarter
            screen.blit(win_text, win_text_rect)
            
            # Display final score
            final_score_text = FONT_LARGE.render(f"Final Score: {zombie_kill_count} Zombies Killed", True, (255, 255, 0))
            final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 4 + 80))
            screen.blit(final_score_text, final_score_rect)
            
            # Still show animation if available
            if scaled_win_gif_frames and len(scaled_win_gif_frames) > 0:
                win_frame_index += win_animation_speed
                if win_frame_index >= len(scaled_win_gif_frames):
                    win_frame_index = 0

                current_frame = scaled_win_gif_frames[int(win_frame_index) % len(scaled_win_gif_frames)]
                frame_rect = current_frame.get_rect(center=(screen_width // 2, screen_height // 2 + 50))  # Position lower
                screen.blit(current_frame, frame_rect)
             # Always display the win text
            win_text = FONT_GAMEOVER.render("YOU WIN!", True, (0, 255, 0))
            win_text_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 4))  # Position at top quarter
            screen.blit(win_text, win_text_rect)
            

        elif game_over:
            # Handle game-over animation

            game_over_text = FONT_GAMEOVER.render("GAME OVER", True, (255, 0, 0))
            game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(game_over_text, game_over_text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Run the game
if __name__ == "__main__":
    main()
