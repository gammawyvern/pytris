import pygame as pg;
import numpy as np;
from enum import Enum;

class TetrominoType(Enum):

    I = [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]

    O = [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]

    L = [[0, 0, 1, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    J = [[1, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    T = [[0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    S = [[0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

    Z = [[1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

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
        self.shape = list(tetromino_type.value); 

    def rotate(self, right=True):
        rot_dir = -1 if right else 1;
        self.shape = np.rotate90(self.shape, k=rot_dir);

    def draw(self, screen):
        # TODO Update this later
        # It will crash currently if called
        screen.blit(self.image, self.rect);
