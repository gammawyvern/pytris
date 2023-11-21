import pygame as pg;
from pygame import Vector2;
import numpy as np;
from enum import Enum;

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

class Tetromino(pg.sprite.Sprite):
    def __init__(self, tetromino_type: TetrominoType, game):
        self.game = game;
        self.type = tetromino_type;
        self.shape = np.copy(tetromino_type.value[0]); 
        self.color = tetromino_type.value[1];
        self.offset = Vector2((self.game.width/2)-2, 0);

    def rotate(self, right=True):
        rot_dir = -1 if right else 1;
        rot_shape = np.rot90(self.shape, k=rot_dir);

        # Check for collisions
        for row in range(4):
            for col in range(4):
                cell_x = (self.offset.x + col);
                cell_y = (self.offset.y + row);
                if (rot_shape[row, col] == 1 and
                    (cell_x >= self.game.width or cell_x < 0 or
                     cell_y >= self.game.height or cell_y < 0)):
                    # TODO add rotation logic instead of just stopping it alltogther
                    return;
                if (rot_shape[row, col] == 1 and
                    self.game.game_board[int(cell_y), int(cell_x)]):
                    # TODO add rotation logic instead of just stopping it alltogther
                    return;
        
        self.shape = rot_shape;


    def shift(self, right=True):
        x_shift = 1 if right else -1;

        # Check for another piece
        for row in range(4):
            for col in range(4):
                # Pos of potential collision
                cell_x = (self.offset.x + col + x_shift);  
                cell_y = (self.offset.y + row);
                if (self.shape[row, col] == 1 and
                    (cell_x >= self.game.width or cell_x < 0)):
                    return;
                if (self.shape[row, col] == 1 and
                    self.game.game_board[int(cell_y), int(cell_x)]):
                    return;

        self.offset += Vector2(x_shift, 0);

    # Return if it fell
    def fall(self) -> bool:
        # Find row bottom of piece
        bottom_row = 3;
        while np.all(self.shape[bottom_row] == 0) and bottom_row >= 0:
            bottom_row -= 1;
        # Check for bottom of board
        if (self.offset.y + bottom_row) >= (self.game.height - 1):
            return False;

        # Check for another piece
        for row in range(4):
            for col in range(4):
                # Pos of potential collision
                cell_x = (self.offset.x + col) % self.game.width;  
                cell_y = (self.offset.y + row + 1);
                if (self.shape[row, col] == 1 and
                    self.game.game_board[int(cell_y), int(cell_x)]):
                    return False;

        self.offset += Vector2(0, 1);
        return True;

    @property
    def offset(self):
        return Vector2(
            # TODO for now remove % self.game.width/height
            self.__offset.x,
            self.__offset.y,
        );

    @offset.setter
    def offset(self, val):
        # TODO for now remove % self.game.width/height
        self.__offset = Vector2(
            val.x,
            val.y,
        );



