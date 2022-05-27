"""
PySnake settings file
- This file customizes the various settings that will be used in the game
"""

# Speed settings
# This setting changes the minimum time between each refresh
# The units in this speed settings are all in milliseconds (ms)
# Please do not input negative speed
SPEED_CAP = 250
STARTING_SPEED = 500

# Grid settings
# This means the snake will have to move in a 8 by 8 grid by default
# We must have at least 2 rows and columns for the game to be played
ROW = 12
COLUMN = 12

# Color settings
SNAKE_COLOR = 'white'
APPLE_COLOR = 'red'
BACKGROUND_COLOR = 'black'
GRID_COLOR = 'white'

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
