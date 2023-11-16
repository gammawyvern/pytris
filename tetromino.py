import pygame as pg;
from pygame import Vector2;
import numpy as np;
from enum import Enum;

class TetrominoType(Enum):

    I = [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]];

    O = [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]];

    L = [[0, 0, 1, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]];

    J = [[1, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]];

    T = [[0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]];

    S = [[0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]];

    Z = [[1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]];

    '''
    I = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    O = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    L = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    J = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    S = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    Z = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    T = pg.image.load(os.path.join('assets', 'Tetrominos.png'));
    '''

class Tetromino(pg.sprite.Sprite):
    def __init__(self, tetromino_type: TetrominoType):
        self.type = tetromino_type;
        self.shape = np.copy(tetromino_type.value); 
        self.offset = Vector2(0, 0);

    def rotate(self, right=True):
        rot_dir = -1 if right else 1;
        self.shape = np.rot90(self.shape, k=rot_dir);

    def shift(self, right=True):
        left = not right;

        # TODO magic numbers are for default size board [20, 10]
        x_shift = 1 if right else -1;

        # Check for out of bounds
        # TODO could break if tetromino shape was empty
        left_bound = int(self.offset.x);
        right_bound = int(self.offset.x + 3);
        if left and left_bound <= 0:
            overflow_col = 1 + abs(left_bound);
            if not np.all(self.shape[:, 0:overflow_col] == 0):
                x_shift = 0;
        elif right and right_bound >= 9:
            overflow_col = 3 - abs(9 - right_bound);
            if not np.all(self.shape[:, overflow_col:4] == 0):
                x_shift = 0;

        self.offset += Vector2(x_shift, 0);

    # Return if it fell
    def fall(self) -> bool:
        # TODO for now just deal with bottom of board
        bottom_bound = int(self.offset.y + 3);
        if bottom_bound >= 19:
            overflow_row = 3 - (abs(19 - bottom_bound));
            if not np.all(self.shape[overflow_row:4, :] == 0):
                return False;

        self.offset += Vector2(0, 1);
        return True;

    def draw(self, screen):
        # TODO Even needed?
        screen.blit(self.image, self.rect);

