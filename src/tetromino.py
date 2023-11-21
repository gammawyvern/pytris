import pygame as pg;
import numpy as np;
import enum;
import copy;

class TetrominoType(enum.Enum):

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
        self.offset = pg.Vector2((self.game.width/2)-2, 0);

    ####################################
    # Public movement wrapper functions.
    # Only moves Tetromino if movement
    # is valid.
    ####################################
 
    def fall(self, right=True) -> bool:
        return self.__move_with_collision(Tetromino.__fall, right=right);

    def rotate(self, right=True) -> bool:
        return self.__move_with_collision(Tetromino.__rotate, right=right);

    def shift(self, right=True) -> bool:
        return self.__move_with_collision(Tetromino.__shift, right=right);

    ####################################
    # Safe movement function. Ensures
    # there will be no collisions
    # before performing movement.
    ####################################

    def __move_with_collision(self, move_func, right=True) -> bool:
        copy_tet: Tetromino = copy.copy(self);
        move_func(copy_tet, right=right);

        for row_index, row in enumerate(copy_tet.shape):
            for col_index, cell in enumerate(row):
                board_x = int(copy_tet.offset.x + col_index);
                board_y = int(copy_tet.offset.y + row_index);

                # Out of bounds detection
                oob_hori = board_x < 0 or board_x >= copy_tet.game.width;
                oob_vert = board_y < 0 or board_y >= copy_tet.game.height;
                if (cell == 1 and (oob_hori or oob_vert)):
                    return False;
                # Other board blocks detection
                if (cell == 1 and copy_tet.game.game_board[board_y, board_x]):
                    return False;
        
        move_func(self, right=right);
        return True;

    ####################################
    # Private movement functions
    # (Unsafe!). Call public versions
    # instead, which use
    # __move_with_collision() to
    # check if movement is valid.
    ####################################

    def __fall(self, right=True):
        self.offset += pg.Vector2(0, 1);

    def __rotate(self, right=True):
        rot_dir = -1 if right else 1;
        self.shape = np.rot90(self.shape, k=rot_dir);

    def __shift(self, right=True):
        x_shift = 1 if right else -1;
        self.offset += pg.Vector2(x_shift, 0);

    ####################################
    # Getters / Setters
    ####################################

    @property
    def offset(self):
        return pg.Vector2(
            self.__offset.x,
            self.__offset.y,
        );

    @offset.setter
    def offset(self, val):
        self.__offset = pg.Vector2(
            val.x,
            val.y,
        );
