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
        self.__game = game;
        self.__type = tetromino_type;
        self.__shape = np.copy(tetromino_type.value[0]); 
        self.__color = pg.Color(tetromino_type.value[1]);
        self.__offset = pg.Vector2((self.__game.width/2)-2, 0);

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

        for row_index, row in enumerate(copy_tet.__shape):
            for col_index, cell in enumerate(row):
                board_x = int(copy_tet.__offset.x + col_index);
                board_y = int(copy_tet.__offset.y + row_index);

                # Out of bounds detection
                oob_hori = board_x < 0 or board_x >= copy_tet.__game.width;
                oob_vert = board_y < 0 or board_y >= copy_tet.__game.height;
                if (cell == 1 and (oob_hori or oob_vert)):
                    return False;
                # Other board blocks detection
                if (cell == 1 and copy_tet.__game.game_board[board_y, board_x]):
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
        self.__offset += pg.Vector2(0, 1);

    def __rotate(self, right=True):
        rot_dir = -1 if right else 1;
        self.__shape = np.rot90(self.__shape, k=rot_dir);

    def __shift(self, right=True):
        x_shift = 1 if right else -1;
        self.__offset += pg.Vector2(x_shift, 0);


    ####################################
    # Ghost functionality
    ####################################

    def get_ghost(self):
        ghost = copy.copy(self);
        ghost.__color = pg.Color(255, 255, 255);
        while ghost.fall():
            pass;

        return ghost;
    
    ####################################
    # Getters / Setters
    ####################################

    @property
    def offset(self):
        return pg.Vector2(
            self.__offset.x,
            self.__offset.y
        )

    @property
    def shape(self):
        return np.copy(self.__shape);

    @property
    def color(self):
        return pg.Color(self.__color);

    ####################################
    # Copy thing
    ####################################

    def __copy__(self):
        copy_tet = Tetromino(self.__type, self.__game);
        copy_tet.__offset = self.offset;
        copy_tet.__shape = self.shape;
        return copy_tet;



