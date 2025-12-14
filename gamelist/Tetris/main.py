import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 30
COLUMNS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),   # I
    (0, 0, 255),     # J
    (255, 165, 0),   # L
    (255, 255, 0),   # O
    (0, 255, 0),     # S
    (255, 0, 0),     # Z
    (128, 0, 128)    # T
]

# Shapes with rotations
SHAPES = [
    # I
    [
        [[1,1,1,1]],
        [[1],[1],[1],[1]]
    ],
    # J
    [
        [[1,0,0],[1,1,1]],
        [[1,1],[1,0],[1,0]],
        [[1,1,1],[0,0,1]],
        [[0,1],[0,1],[1,1]]
    ],
    # L
    [
        [[0,0,1],[1,1,1]],
        [[1,0],[1,0],[1,1]],
        [[1,1,1],[1,0,0]],
        [[1,1],[0,1],[0,1]]
    ],
    # O
    [
        [[1,1],[1,1]]
    ],
    # S
    [
        [[0,1,1],[1,1,0]],
        [[1,0],[1,1],[0,1]]
    ],
    # Z
    [
        [[1,1,0],[0,1,1]],
        [[0,1],[1,1],[1,0]]
    ],
    # T
    [
        [[0,1,0],[1,1,1]],
        [[1,0],[1,1],[1,0]],
        [[1,1,1],[0,1,0]],
        [[0,1],[1,1],[0,1]]
    ]
]

# Create the grid
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid


class Piece:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]


def convert_shape_format(piece):
    positions = []
    layout = piece.image()

    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            if val == 1:
                positions.append((piece.x + j, piece.y + i))
    return positions


def valid_space(piece, grid):
    accepted = [(x, y) for y in range(ROWS) for x in range(COLUMNS) if grid[y][x] == BLACK]
    for pos in convert_shape_format(piece):
        x, y = pos
        if x < 0 or x >= COLUMNS or y >= ROWS:
            return False
        if (x, y) not in accepted and y >= 0:
            return False
    return True


def check_lost(positions):
    for (x, y) in positions:
        if y < 1:
            return True
    return False


def clear_rows(grid, locked):
    cleared = 0
    for i in range(ROWS - 1, -1, -1):
        if BLACK not in grid[i]:
            cleared += 1
            for x in range(COLUMNS):
                if (x, i) in locked:
                    del locked[(x, i)]
            for y2 in range(i - 1, -1, -1):
                for x2 in range(COLUMNS):
                    if (x2, y2) in locked:
                        locked[(x2, y2 + 1)] = locked.pop((x2, y2))
    return cleared


def draw_grid(surface, grid):
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for x in range(COLUMNS):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))


def draw_window(surface, grid, score):
    surface.fill(BLACK)
    draw_grid(surface, grid)

    font = pygame.font.SysFont("comicsans", 30)
    label = font.render(f"Score: {score}", True, WHITE)
    surface.blit(label, (10, 10))

    pygame.display.update()


def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    current_piece = Piece(5, 0, random.randrange(len(SHAPES)))
    next_piece = Piece(5, 0, random.randrange(len(SHAPES)))

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    run = True
    while run:

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Gravity
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1

            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[(pos[0], pos[1])] = current_piece.color

                current_piece = next_piece
                next_piece = Piece(5, 0, random.randrange(len(SHAPES)))
                score += clear_rows(grid, locked_positions) * 10

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        # Draw falling piece
        for x, y in convert_shape_format(current_piece):
            if y >= 0:
                grid[y][x] = current_piece.color

        draw_window(win, grid, score)

        if check_lost(locked_positions):
            run = False

    pygame.quit()


if __name__ == "__main__":
    main()