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

class Tetromino(pg.sprite.Sprite):
    def __init__(self, tetromino_type: TetrominoType, board):
        self.board = board;
        self.type = tetromino_type;
        self.shape = np.copy(tetromino_type.value); 
        self.offset = Vector2(0, 0);

    def rotate(self, right=True):
        rot_dir = -1 if right else 1;
        self.shape = np.rot90(self.shape, k=rot_dir);

    def shift(self, right=True):
        x_shift = 1 if right else -1;
        self.offset += Vector2(x_shift, 0);

    # Return if it fell
    def fall(self) -> bool:
        # TODO reimplement
        self.offset += Vector2(0, 1);
        return True;

    @property
    def offset(self):
        return Vector2(
            self.__offset.x % self.board.width,
            self.__offset.y % self.board.height,
        );

    @offset.setter
    def offset(self, val):
        self.__offset = Vector2(
            val.x % self.board.width,
            val.y % self.board.height,
        );
