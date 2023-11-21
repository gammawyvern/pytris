import pygame as pg;
from pygame import Vector2;
import numpy as np;
from enum import Enum;
import copy;

class TetrominoType(Enum):

    I = ([[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]],
         (0, 128, 128));

    O = ([[0, 0, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
         (255, 255, 0));

    L = ([[0, 0, 1, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
         (255, 165, 0));

    J = ([[1, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
         (0, 0, 255));

    T = ([[0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
         (128, 0, 128));

    S = ([[0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
         (0, 255, 0));

    Z = ([[1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
         (255, 0, 0));

class Tetromino:
    def __init__(self, tetromino_type: TetrominoType, game):
        self.game = game;
        self.type = tetromino_type;
        self.shape = np.copy(tetromino_type.value[0]); 
        self.color = tetromino_type.value[1];
        self.offset = Vector2((self.game.width/2)-2, 0);
 
    def fall(self, right=True) -> bool:
        return self.__move_with_collision(Tetromino.__fall, right=right);

    def rotate(self, right=True) -> bool:
        return self.__move_with_collision(Tetromino.__rotate, right=right);

    def shift(self, right=True) -> bool:
        return self.__move_with_collision(Tetromino.__shift, right=right);

    # Perform movement on copy and then look for collisions
    # movement is a function (either rotate(), shift(), or fall())
    def __move_with_collision(self, move_func, right=True) -> bool:
        copy_tet: Tetromino = copy.copy(self);
        move_func(copy_tet, right=right);

        # Check for collisions
        for row in range(4):
            for col in range(4):
                cell_x = copy_tet.offset.x + col;
                cell_y = copy_tet.offset.y + row;
                # Check for out of bounds
                if (copy_tet.shape[row, col] == 1 and
                    (cell_x >= copy_tet.game.width or cell_x < 0 or
                     cell_y >= copy_tet.game.height or cell_y < 0)):
                    return False;
                # Check for other blocks
                if (copy_tet.shape[row, col] == 1 and
                    copy_tet.game.game_board[int(cell_y), int(cell_x)]):
                    return False;
        
        move_func(self, right=right);
        return True;

    def __fall(self, right=True):
        self.offset += Vector2(0, 1);

    def __rotate(self, right=True):
        rot_dir = -1 if right else 1;
        self.shape = np.rot90(self.shape, k=rot_dir);

    def __shift(self, right=True):
        x_shift = 1 if right else -1;
        self.offset += Vector2(x_shift, 0);

    @property
    def offset(self):
        return Vector2(
            self.__offset.x,
            self.__offset.y,
        );

    @offset.setter
    def offset(self, val):
        self.__offset = Vector2(
            val.x,
            val.y,
        );
