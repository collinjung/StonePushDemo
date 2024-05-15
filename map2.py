import pygame
import sys
import os



# Initialize Pygame
pygame.init()

# Grid dimensions
GRID_WIDTH = 12
GRID_HEIGHT = 7
TILE_SIZE = 40

# Screen dimensions based on grid size
WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Game")

# Initial positions
initial_player_pos = [0, 3]
red_stone_pos = [5, 2]
green_stone_pos = [5, 4]
goal_red_space = [11,6]
goal_green_space = [11, 0]

player_pos = initial_player_pos.copy()

stones = {
    "red": red_stone_pos.copy(),
    "green": green_stone_pos.copy(),
}

goals = {
    "goal_red": goal_red_space,
    "goal_green": goal_green_space,
}

walls = [
    [3, 0], 
    [7, 1], [8, 1],
    [2, 2], [3, 2], [4, 2], [6, 2], [7, 2], [8, 2], [9, 2],
    [6, 3], [7, 3], [8, 3], [9, 3],
    [2, 4], [3, 4], [4, 4], [6, 4], [7, 4], [8, 4], [9, 4],
    [7, 5], [8, 5],
    [3, 6], 
]

game_over = False

history = []

def draw_grid():
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_player():
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLUE, player_rect)

def draw_stones():
    colors = {"red": RED, "green": GREEN}
    for color, pos in stones.items():
        stone_center = (pos[0] * TILE_SIZE + TILE_SIZE // 2, pos[1] * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(screen, BLACK, stone_center, TILE_SIZE // 2)
        pygame.draw.circle(screen, colors[color], stone_center, TILE_SIZE // 2 - 2)

def draw_goals():
    colors = {"goal_red": RED, "goal_green": GREEN}
    for color, pos in goals.items():
        goal_rect = pygame.Rect(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, colors[color], goal_rect)

def draw_walls():
    for wall in walls:
        wall_rect = pygame.Rect(wall[0] * TILE_SIZE, wall[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, BLACK, wall_rect)

def is_occupied(x, y, ls):
    return [x, y] in ls

def move_position(position, direction):
    new_pos = position.copy()
    if direction == pygame.K_UP:
        new_pos[1] -= 1
    elif direction == pygame.K_DOWN:
        new_pos[1] += 1
    elif direction == pygame.K_LEFT:
        new_pos[0] -= 1
    elif direction == pygame.K_RIGHT:
        new_pos[0] += 1
    return new_pos

def is_within_bounds(position):
    return 0 <= position[0] < GRID_WIDTH and 0 <= position[1] < GRID_HEIGHT

def save_history():
    history.append((player_pos.copy(), {color: pos.copy() for color, pos in stones.items()}))

def move_player(key):
    if game_over:
        return

    save_history()

    new_pos = move_position(player_pos, key)
    
    if is_within_bounds(new_pos) and not is_occupied(new_pos[0], new_pos[1], walls):
        if is_occupied(new_pos[0], new_pos[1], stones.values()):
            stone_color = [color for color, pos in stones.items() if pos == new_pos][0]
            new_stone_pos = move_position(new_pos, key)

            if is_within_bounds(new_stone_pos) and not is_occupied(new_stone_pos[0], new_stone_pos[1], list(stones.values()) + walls):
                stones[stone_color] = new_stone_pos
                player_pos[:] = new_pos
        else:
            player_pos[:] = new_pos

    screen.fill(WHITE)
    draw_grid()
    draw_goals()
    draw_walls()
    draw_stones()
    draw_player()
    pygame.display.flip()

    check_success()

def check_success():
    global game_over
    if (stones["red"] == goals["goal_red"] and
        stones["green"] == goals["goal_green"]):
        game_over = True
        announce_success()

def announce_success():
    font = pygame.font.SysFont(None, 74)
    text = font.render('Success!', True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds to ensure the message is visible

def undo_move():
    global player_pos, stones
    if history:
        player_pos, stones = history.pop()

def reset_game():
    global player_pos, stones, game_over, history
    player_pos = initial_player_pos.copy()
    stones = {
        "red": red_stone_pos.copy(),
        "green": green_stone_pos.copy(),
    }
    game_over = False
    history.clear()

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_z:
                    undo_move()
                else:
                    move_player(event.key)

    screen.fill(WHITE)
    draw_grid()
    draw_goals()
    draw_walls()
    draw_stones()
    draw_player()
    pygame.display.flip()
