"""Allows creation of and control of Tetrominos.

This module allows for creating and controlling of 
Tetrominos for use in the Pytris game. Tetrominos 
hold a reference to a game, but are not actually 
on the board in that game. Instead they are overlayed 
onto the board and check the board for collisions.

"""

import pygame as pg;
import numpy as np;
import enum;
import copy;

class TetrominoType(enum.Enum):
    """Represents each type of Tetromino in Tetris.
        
    Each variant's value is a tuple. The first element 
    is a 4x4 array with its respective Tetromino's shape 
    in its default orientation; the second element is
    it's respective Tetromino color as an RGB tuple.
    """

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
    """Represents a controllable Tetromino in a Pytris game.

    Tetromino is created from base shape from TetrominoType.
    It always holds a reference to a valid game that it uses
    for collision checks. It also spawns at the top middle 
    of the game.

    Use fall(), shift(), rotate(), or reset() to control 
    Tetromino. It will only perform the action if it results 
    in no collision. reset() will return Tetromino to default 
    orientiation and position at top of screen.
    """

    def __init__(self, tetromino_type: TetrominoType, game):
        """Initializes a Tetromino from a specified type.

        Args:
            tetromino_type:
                One of the 7 TetrominoType variants that 
                corresponds to a Tetromino.
            game:
                A Pytris instance that the Tetromino will 
                use for collision detection.
        """
        self.__game = game;
        self.__type = tetromino_type;
        self.__shape = np.copy(tetromino_type.value[0]); 
        self.__color = pg.Color(tetromino_type.value[1]);
        self.__offset = pg.Vector2((self.__game.width/2)-2, 0);

    def reset(self):
        """Resets Tetromino to post initialization state."""
        self.__shape = np.copy(self.__type.value[0]); 
        self.__offset = pg.Vector2((self.__game.width/2)-2, 0);

    ####################################
    # Public movement wrapper functions.
    # Only moves Tetromino if movement
    # is valid.
    ####################################
 
    def fall(self, right=True) -> bool:
        """Moves Tetromino one block down.

        Args:
            right: Ignored.

        Returns:
            bool:
                True if Tetromino was moved (no collision occured)
                False if Tetromino was not moved (collision occured)
        """
        return self.__move_with_collision(Tetromino.__fall, right=right);

    def rotate(self, right=True) -> bool:
        """Rotates Tetromino shape 90 degrees.

        Rotates the shape of the Tetromino within its 4x4 array 
        if there is no collision.

        Args:
            right:
                True: Rotate 90 degrees clockwise.
                False: Rotate 90 degrees counter-clockwise.

        Returns:
            bool:
                True if Tetromino was moved (no collision occured).
                False if Tetromino was not moved (collision occured).
        """
        return self.__move_with_collision(Tetromino.__rotate, right=right);

    def shift(self, right=True) -> bool:
        """Moves Tetromino one block right or left

        Args:
            right:
                True: Move Tetromino right.
                False: Move Tetromino left.

        Returns:
            bool:
                True if Tetromino was moved (no collision occured).
                False if Tetromino was not moved (collision occured).
        """
        return self.__move_with_collision(Tetromino.__shift, right=right);

    ####################################
    # Safe movement function. Ensures
    # there will be no collisions
    # before performing movement.
    ####################################

    def __move_with_collision(self, move_func, right=True) -> bool:
        """Runs movement function if no collision will occur.

        Creates a copy of the Tetromino, and runs the passed private
        movement function on the copy. If that copy then has no 
        collisions, the movement is also run on the original
        Tetromino.

        Args:
            move_func: __fall(), __shift(), or __rotate()
            right: bool passed to move_func

        Returns:
            bool: 
                True if Tetromino was moved (no collision occured).
                False if Tetromino was not moved (collision occured).
        """
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
        """Creates a representative ghost Tetromino.

        A ghost Tetromino represents where the Tetromio 
        will eventually be placed if the Tetromino is not moved.
        The color is set to white.

        Returns:
            Tetromino: 
                A representative white ghost Tetromino
        """
        ghost = copy.copy(self);
        ghost.__color = pg.Color(255, 255, 255);
        while ghost.fall():
            pass;

        return ghost;
    
    ####################################
    # Getters / Setters
    ####################################

    @property
    def offset(self) -> pg.Vector2:
        """Returns a copy of the Tetromino board position.

        Returns:
            pygame.Vector2:
                Represents the top left corner of the 4x4 Tetromino 
                shape array relative to the game board it holds.
        """
        return pg.Vector2(
            self.__offset.x,
            self.__offset.y
        )

    @property
    def shape(self) -> np.ndarray:
        """Returns a copy of the Tetromino shape array

        Returns:
            numpy.ndarray:
                Contains the shape of the Tetromino in a 4x4 numpy array.
                Empty cells are indicated by a 0, while the blocks are
                represented by a 1.
        """
        return np.copy(self.__shape);

    @property
    def color(self) -> pg.Color:
        """Returns a copy of the Tetromino color.

        Returns:
            pygame.Color:
                Color that each block in the Tetromino shape should be.
        """
        return pg.Color(self.__color);

    def get_middle(self) -> pg.Vector2:
        """Returns offset of middle of Tetromino shape. 

        Checks Tetromino shape to find the center of the actual piece, 
        as many shapes have empty rows and/or columns.

        Returns:
            pygame.Vector2:
                Vector that holds the x and y center of the Tetromino shape.
                It is not by array index, but by the offset from the side.
        """
        left = 0;
        while np.all(self.shape[:, left] == 0):
            left += 1;
        right = 3;
        while np.all(self.shape[:, right] == 0):
            right -= 1;
        top = 0;
        while np.all(self.shape[top, :] == 0):
            top += 1;
        bottom = 3;
        while np.all(self.shape[bottom, :] == 0):
            bottom -= 1;

        center = pg.Vector2((left + right + 1) / 2,
                            (top + bottom + 1) / 2);
        return center;

    ####################################
    # Copy thing
    ####################################

    def __copy__(self):
        """Deep copies Tetromino."""
        copy_tet = Tetromino(self.__type, self.__game);
        copy_tet.__offset = self.offset;
        copy_tet.__shape = self.shape;
        return copy_tet;



