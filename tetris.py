import random
import time
import curses

# Terminal size
WIDTH = 10
HEIGHT = 20

# Tetromino shapes
SHAPES = [
    [
        [1, 1, 1, 1],
    ],
    [
        [1, 1],
        [1, 1],
    ],
    [
        [1, 1, 0],
        [0, 1, 1],
    ],
    [
        [0, 1, 1],
        [1, 1, 0],
    ],
    [
        [1, 1, 1],
        [0, 1, 0],
    ],
    [
        [1, 1, 1],
        [1, 0, 0],
    ],
    [
        [1, 1, 1],
        [0, 0, 1],
    ],
]


def create_board():
    """
    Create the game board with empty cells.
    """
    board = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    return board


def draw_board(stdscr, board, tetromino, x, y):
    """
    Draw the game board in the terminal.
    """
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if (
                row >= y
                and row < y + len(tetromino)
                and col >= x
                and col < x + len(tetromino[0])
            ):
                cell = (
                    tetromino[row - y][col - x]
                    if tetromino[row - y][col - x]
                    else board[row][col]
                )
            else:
                cell = board[row][col]
            if cell == 1:
                stdscr.addch(row, col, "#")
            else:
                stdscr.addch(row, col, str(cell))


def check_collision(board, tetromino, x, y):
    """
    Check if a tetromino collides with the board or other tetrominos.
    """
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col] and (
                x + col < 0
                or x + col >= WIDTH
                or y + row >= HEIGHT
                or board[y + row][x + col] != "."
            ):
                return True
    return False


def rotate_tetromino(tetromino):
    """
    Rotate a tetromino 90 degrees clockwise.
    """
    return list(zip(*reversed(tetromino)))


def clear_rows(board):
    """
    Clear full rows from the board and shift the remaining rows down.
    """
    rows_cleared = 0
    rows_to_clear = []
    for row in range(len(board)):
        if all(cell != "." for cell in board[row]):
            rows_to_clear.append(row)
    for row in rows_to_clear:
        del board[row]
        board.insert(0, ["." for _ in range(WIDTH)])
        rows_cleared += 1
    return rows_cleared


def main(stdscr):
    for i in range(5):
        print(f"get ready in {5-i} seconds\n")
        time.sleep(1)

    # Set up the game
    curses.curs_set(0)
    stdscr.nodelay(1)  # Enable non-blocking keyboard input
    board = create_board()
    tetromino = random.choice(SHAPES)
    x, y = WIDTH // 2 - len(tetromino[0]) // 2, 0
    score = 0
    game_over = False

    # Timer variables
    timer = 0
    start_time = time.time()

    # Main game loop
    while not game_over:
        stdscr.clear()  # Clear the terminal

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Move tetromino down automatically after 10 seconds
        if elapsed_time >= 1 and not check_collision(board, tetromino, x, y + 1):
            y += 1
            start_time = time.time()  # Reset start time

        if check_collision(board, tetromino, x, y + 1):
            # Lock tetromino in place
            for row in range(len(tetromino)):
                for col in range(len(tetromino[row])):
                    if tetromino[row][col]:
                        board[y + row][x + col] = "#"

            # Clear full rows
            rows_cleared = clear_rows(board)
            score += rows_cleared * rows_cleared  # Increase score

            # Select a new tetromino
            tetromino = random.choice(SHAPES)
            x, y = WIDTH // 2 - len(tetromino[0]) // 2, 0

            # Check for game over
            if check_collision(board, tetromino, x, y):
                game_over = True

        # User input
        key = stdscr.getch()
        if key == ord("a") and not check_collision(board, tetromino, x - 1, y):
            x -= 1
        elif key == ord("d") and not check_collision(board, tetromino, x + 1, y):
            x += 1
        elif key == ord("s"):
            if not check_collision(board, tetromino, x, y + 1):
                y += 1
            timer = 0
        elif key == ord("q"):
            game_over = True
        elif key == ord("r"):
            rotated_tetromino = rotate_tetromino(tetromino)
            if not check_collision(board, rotated_tetromino, x, y):
                tetromino = rotated_tetromino

        # Draw the board
        draw_board(stdscr, board, tetromino, x, y)
        stdscr.addstr(HEIGHT, 0, f"Score: {score}")

        # Refresh the screen
        stdscr.refresh()

        # Increment timer
        timer += 1

        # Slow down the game
        time.sleep(0.1)

    stdscr.addstr(HEIGHT + 2, 0, "Game Over")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
