"""
PySnake main gameplay file
This file captures the main game loop and additional menu items we may want
Created by Ray
"""
import pygame
from settings import *
from typing import List, Tuple
import random
import sys

KEY_DICT = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}


class InvalidGridSizeException(Exception):
    """The exception that will be raised when settings.py contains invalid settings"""
    def __str__(self) -> str:
        """The information given when this exception is raised"""
        return 'The grid size is invalid! Check settings.py perhaps?'


class SnakeBoard(object):
    """This is the class object of a snake board

    Description of attributes:
    - self._board has 3 possible items contained in it:
        - 'S1' which represents the head of the snake
        - 'S0' which represents the body of the snake
        - 'A' which represents an apple is contained in that tile
        - 'N' which represents that we have nothing in that tile
        We can access a tile by using self._board[i][j], which represents what we have at the
        i-th row, j-th tile

    - self._snake_direction is a tuple that denotes the
    (Horizontal displacement, Vertical displacement)

    - self._snake_row and self._snake_col tells us where the snake is located

    - self._snake is a list that represents all of the locations where the snake
    head had been through

    - self._snake_length is an integer that represents the length of the snake currently

    - self._end tells us if the game has ended or not

    - self._move_lock locks the change of direction until a move is conducted

    Representation Invariants:
        - self._snake_direction in {(1, 0), (-1, 0), (0, 1), (0, -1))}
        - all(self._board[r][c] in {'S1', 'S0'} for r, c in self._snake)

    """
    _row: int
    _col: int
    _board: List[List[str]]
    _snake_direction: Tuple[int, int]
    _snake_row: int
    _snake_col: int
    _snake: List[Tuple[int, int]]
    _snake_length: int
    _end: bool
    _apple_row: int
    _apple_col: int
    _move_lock: bool

    def __init__(self, row: int, col: int) -> None:
        """This method generates a board object with the given row and column parameters"""
        if row < 2 or col < 2:
            raise InvalidGridSizeException

        self._row = row
        self._col = col
        self._board = [['N' for _ in range(col)] for _ in range(row)]

        # Initialize the default direction to None
        self._snake_direction = (0, 0)

        self._end = False

        # Generating a random snake location
        snake_row = random.randint(0, self._row - 1)
        snake_col = random.randint(0, self._col - 1)

        self._snake_row = snake_row
        self._snake_col = snake_col
        self._snake = [(self._snake_row, self._snake_col)]

        self._board[snake_row][snake_col] = 'S1'
        self._snake_length = 1

        self.generate_apple()

        self._move_lock = False

    def get_apple(self) -> Tuple[int, int]:
        """Returns the location of the apple in this grid"""
        return (self._apple_row, self._apple_col)

    def get_row(self) -> int:
        """Return the row of this grid"""
        return self._row

    def get_col(self) -> int:
        """Return the col of this grid"""
        return self._col

    def get_length(self) -> int:
        """Returns the score, or the length of the snake"""
        return self._snake_length

    def get_direction(self) -> Tuple[int, int]:
        """Returns the direction that the snake is going in"""
        return self._snake_direction

    def get_path(self) -> List[Tuple[int, int]]:
        """Returns the path that the snake had travelled through"""
        return self._snake

    def get_end(self) -> bool:
        """Returns if the game has ended or not"""
        return self._end

    def generate_apple(self) -> None:
        """Generates the apple at a random location inside this game board"""
        # Generates the apple at a point where it is empty
        while True:
            apple_row = random.randint(0, self._row - 1)
            apple_col = random.randint(0, self._col - 1)

            if self._board[apple_row][apple_col] == 'N':
                break

        self._board[apple_row][apple_col] = 'A'

        self._apple_row = apple_row
        self._apple_col = apple_col

    def update_direction(self, direction: Tuple[int, int]) -> None:
        """Changes the direction of the snake"""
        if self._move_lock:
            return

        # For the initial setup
        if self._snake_direction == (0, 0):
            self._snake_direction = direction

        h_direction, v_direction = direction

        if not (int(h_direction * -1) == self._snake_direction[0] or
                int(v_direction * -1) == self._snake_direction[1]):
            self._snake_direction = direction
            self._move_lock = True

    def next(self) -> bool:
        """This method makes the game proceed by 1 tick, that is, process what happens in this
        new frame state

        It returns a bool, which signifies if the game ended or not, after we processed this frame
        state

        Returning True means the game had stopped, returning False means the game hasn't ended yet
        """
        self._move_lock = False

        new_snake_row = self._snake_row + self._snake_direction[1]
        new_snake_col = self._snake_col + self._snake_direction[0]

        # If crashes into wall
        if not (0 <= new_snake_row < self._row) or not (0 <= new_snake_col < self._col):
            self._end = True
            return True

        # If crashes into itself
        if self._board[new_snake_row][new_snake_col] == 'S0':
            self._end = True
            return True

        self._board[self._snake_row][self._snake_col] = 'N'

        self._snake_row = new_snake_row
        self._snake_col = new_snake_col

        self._snake.append((new_snake_row, new_snake_col))

        # Only keep up to 2 times the snake's length's path
        if len(self._snake) > self._snake_length + 1:
            self._snake.pop(0)

        ate_apple = self._board[new_snake_row][new_snake_col] == 'A'

        if ate_apple:
            self._snake_length += 1

        self._board[new_snake_row][new_snake_col] = 'S1'

        for i in range(2, self._snake_length + 1):
            segment_r = self._snake[-i][0]
            segment_c = self._snake[-i][1]

            self._board[segment_r][segment_c] = 'S0'

        for i in range(len(self._snake) - self._snake_length - 1, -1, -1):
            empty_r = self._snake[i][0]
            empty_c = self._snake[i][1]

            self._board[empty_r][empty_c] = 'N'

        if ate_apple:
            self.generate_apple()

    def __str__(self) -> str:
        """Returns a string representation of our Snake game"""
        s = ''

        for row in self._board:
            s += '\t'.join(row)
            s += '\n'

        return s


def initialize_screen() -> pygame.Surface:
    """Initialize pygame and the display window."""
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # White window size background
    screen.fill(pygame.colordict.THECOLORS[BACKGROUND_COLOR])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + [pygame.KEYDOWN, pygame.KEYUP])

    return screen


def draw_grid(screen: pygame.Surface, board: SnakeBoard) -> None:
    """Draws the Grid of the actual game"""
    width, height = screen.get_size()

    row, col = board.get_row(), board.get_col()

    actual_height = 0.8 * height

    # We want to keep the top 15% of the screen to display key information like score.
    vertical_start = 0.15 * height

    square_length = actual_height / row

    horizontal_start = (width - square_length * col) / 2

    # Draw gridlines
    for i in range(row):
        for j in range(col):
            x = horizontal_start + square_length * j
            y = vertical_start + square_length * i

            rect = pygame.Rect(x, y, square_length, square_length)
            pygame.draw.rect(screen, pygame.colordict.THECOLORS[GRID_COLOR], rect, 1)

    pygame.display.flip()


def draw_snake(screen: pygame.Surface, board: SnakeBoard) -> None:
    """Draws the snake in the grid we drew earlier"""
    width, height = screen.get_size()

    row, col = board.get_row(), board.get_col()

    actual_height = 0.8 * height

    # We want to keep the top 15% of the screen to display key information like score.
    vertical_start = 0.15 * height

    square_length = actual_height / row

    horizontal_start = (width - square_length * col) / 2

    locations = board.get_path()[len(board.get_path()) - board.get_length():]

    old_locations = board.get_path()[:len(board.get_path()) - board.get_length()]

    # Draw the snake
    for r, c in locations:
        x = horizontal_start + square_length * c + (square_length / 2)
        y = vertical_start + square_length * r + (square_length / 2)

        rect = pygame.Rect(0, 0, square_length * 0.7, square_length * 0.7)
        rect.center = (x, y)

        pygame.draw.rect(screen, pygame.colordict.THECOLORS[SNAKE_COLOR], rect)

    for r, c in old_locations:
        x = horizontal_start + square_length * c + (square_length / 2)
        y = vertical_start + square_length * r + (square_length / 2)

        rect = pygame.Rect(0, 0, square_length * 0.9, square_length * 0.9)
        rect.center = (x, y)

        pygame.draw.rect(screen, pygame.colordict.THECOLORS[BACKGROUND_COLOR], rect)

    pygame.display.flip()


def draw_apple(screen: pygame.Surface, board: SnakeBoard) -> None:
    """Draws the apple in the grid we generated earlier"""
    width, height = screen.get_size()

    row, col = board.get_row(), board.get_col()

    actual_height = 0.8 * height

    # We want to keep the top 15% of the screen to display key information like score.
    vertical_start = 0.15 * height

    square_length = actual_height / row

    horizontal_start = (width - square_length * col) / 2

    x = horizontal_start + square_length * board.get_apple()[1] + (square_length / 2)
    y = vertical_start + square_length * board.get_apple()[0] + (square_length / 2)

    rect = pygame.Rect(0, 0, square_length * 0.6, square_length * 0.6)
    rect.center = (x, y)

    pygame.draw.rect(screen, pygame.colordict.THECOLORS[APPLE_COLOR], rect)

    pygame.display.flip()


def draw_score(screen: pygame.Surface, board: SnakeBoard) -> None:
    """Draws the score at the top of the screen"""
    width, height = screen.get_size()

    font_size = min(width, height) // 20

    font = pygame.font.SysFont('inconsolata', font_size)
    text_surface = font.render(f'Score: {board.get_length() - 1}',
                               True, pygame.colordict.THECOLORS[SNAKE_COLOR])

    text_rect = text_surface.get_rect()

    text_rect.center = (width // 2, int(height * 0.075))

    pygame.draw.rect(screen, pygame.colordict.THECOLORS['black'], text_rect)

    screen.blit(text_surface, text_rect)


def handle_events(board: SnakeBoard) -> None:
    """Handles pygame events

    The pygame key down event has the following important attribute:
        - event.key: The key that was being pressed, we can utilize this to update stuff

    Just edits the board snake direction state
    """
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.display.quit()

            pygame.quit()

            sys.exit()

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or
                    event.key == pygame.K_DOWN or
                    event.key == pygame.K_LEFT or
                    event.key == pygame.K_RIGHT):
                board.update_direction(KEY_DICT[event.key])


def main() -> None:
    """Runs the actual game"""
    pygame.init()

    screen = initialize_screen()

    board = SnakeBoard(ROW, COLUMN)

    pygame.display.set_caption(f'PySnake v1.0')

    draw_score(screen, board)

    draw_grid(screen, board)

    draw_snake(screen, board)

    draw_apple(screen, board)

    game_start = False

    delay = STARTING_SPEED

    score = [0, 0]

    while not game_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or
                        event.key == pygame.K_DOWN or
                        event.key == pygame.K_LEFT or
                        event.key == pygame.K_RIGHT):

                    board.update_direction(KEY_DICT[event.key])

                    game_start = True

    while True:
        if board.get_end():
            break

        draw_snake(screen, board)

        draw_apple(screen, board)

        draw_score(screen, board)

        handle_events(board)

        score.append(board.get_length())

        score.pop(0)

        # If we detect a change in score
        if score[1] != score[0]:
            draw_score(screen, board)

        if delay > SPEED_CAP:
            delay = int(STARTING_SPEED * (0.85 ** board.get_length()))

        pygame.time.wait(delay)

        pygame.display.flip()

        board.next()

    print(f'Your final score is {board.get_length() - 1}!')

    input('Press enter in the console to close the program!')

    pygame.display.quit()

    pygame.quit()

    sys.exit()


if __name__ == '__main__':
    main()
