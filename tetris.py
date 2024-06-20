import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define Tetris grid dimensions
grid_width = 10
grid_height = 20
grid_size = 30

# Define shapes and their colors
tetrominoes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [0, 1, 0]],  # T
]
tetromino_colors = [CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, MAGENTA]

# Initialize the grid
grid = [[0] * grid_width for _ in range(grid_height)]


def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(
                screen, WHITE, (x * grid_size, y * grid_size, grid_size, grid_size), 1
            )
            if grid[y][x] != 0:
                pygame.draw.rect(
                    screen,
                    tetromino_colors[grid[y][x] - 1],
                    (
                        x * grid_size + 1,
                        y * grid_size + 1,
                        grid_size - 2,
                        grid_size - 2,
                    ),
                )


def draw_tetromino(tetromino, x, y, tetromino_id):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col] == 1:
                pygame.draw.rect(
                    screen,
                    tetromino_colors[tetromino_id - 1],
                    (
                        (x + col) * grid_size + 1,
                        (y + row) * grid_size + 1,
                        grid_size - 2,
                        grid_size - 2,
                    ),
                )


def check_collision(tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col] == 1:
                if (
                    x + col < 0
                    or x + col >= grid_width
                    or y + row >= grid_height
                    or grid[y + row][x + col] != 0
                ):
                    return True
    return False


def clear_rows():
    rows_to_clear = []
    for row in range(grid_height):
        if all(grid[row]):
            rows_to_clear.append(row)

    for row in rows_to_clear:
        del grid[row]
        grid.insert(0, [0] * grid_width)


def game_over():
    pygame.quit()
    quit()


def rotate_tetromino(tetromino):
    return list(zip(*reversed(tetromino)))


def run_tetris():
    clock = pygame.time.Clock()

    tetromino_id = random.randint(1, len(tetrominoes))
    tetromino_x = grid_width // 2 - len(tetrominoes[tetromino_id - 1][0]) // 2
    tetromino_y = 0

    d = str(
        input("Press H for hard E for easy and any key for medium diffulty: ")
    )  # Delay in milliseconds

    delay = 500
    if d == "H":
        delay = 250
    if d == "E":
        delay = 750
    last_move_time = pygame.time.get_ticks()

    game_over_flag = False

    while not game_over_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(
                        tetrominoes[tetromino_id - 1], tetromino_x - 1, tetromino_y
                    ):
                        tetromino_x -= 1

                elif event.key == pygame.K_RIGHT:
                    if not check_collision(
                        tetrominoes[tetromino_id - 1], tetromino_x + 1, tetromino_y
                    ):
                        tetromino_x += 1

                elif event.key == pygame.K_DOWN:
                    while not check_collision(
                        tetrominoes[tetromino_id - 1], tetromino_x, tetromino_y + 1
                    ):
                        tetromino_y += 1

                elif event.key == pygame.K_UP:
                    rotated_tetromino = rotate_tetromino(tetrominoes[tetromino_id - 1])
                    if not check_collision(rotated_tetromino, tetromino_x, tetromino_y):
                        tetrominoes[tetromino_id - 1] = rotated_tetromino

        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > delay:
            last_move_time = current_time
            if not check_collision(
                tetrominoes[tetromino_id - 1], tetromino_x, tetromino_y + 1
            ):
                tetromino_y += 1
            else:
                for row in range(len(tetrominoes[tetromino_id - 1])):
                    for col in range(len(tetrominoes[tetromino_id - 1][row])):
                        if tetrominoes[tetromino_id - 1][row][col] == 1:
                            grid[tetromino_y + row][tetromino_x + col] = tetromino_id

                clear_rows()

                tetromino_id = random.randint(1, len(tetrominoes))
                tetromino_x = (
                    grid_width // 2 - len(tetrominoes[tetromino_id - 1][0]) // 2
                )
                tetromino_y = 0

                if check_collision(
                    tetrominoes[tetromino_id - 1], tetromino_x, tetromino_y
                ):
                    game_over_flag = True

        screen.fill(BLACK)
        draw_grid()
        draw_tetromino(
            tetrominoes[tetromino_id - 1], tetromino_x, tetromino_y, tetromino_id
        )
        pygame.display.update()
        clock.tick(60)

    game_over()



if __name__ == "__main__":
    run_tetris()
