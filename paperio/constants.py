""" Agent Values """
DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))

""" Environment Values """
ROW_COUNT = 80
COLUMN_COUNT = 80

""" Tile Values """
TEMP = -1
UNOCCUPIED = 0
PASSED = 1
OCCUPIED = 2
BOMB = 3
BOOST = 4

""" Rendering Values """
SPRITE_SCALING = 0.5
WIDTH = 10
HEIGHT = 10
MARGIN = 5
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Paper IO Game"
