import pygame as pg;
from pygame import Vector2;
from tetromino import Tetromino, TetrominoType;
import numpy as np;

class Pytris:
    def __init__(self):
        pg.init();
        self.screen = pg.display.set_mode([300, 600]);
        self.clock = pg.time.Clock();

        self.falling_tetromino = None;
        self.running = True;

        # Screen/Draw info
        self.game_array = np.zeros((20, 10));
        self.block_size = 30;

        self.__setup();
        self.__play();
        pg.quit();

    def __setup(self):
        self.falling_tetromino = Tetromino(TetrominoType.I);

    def __play(self):
        while self.running:
            # Read events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False;

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.falling_tetromino.rotate();
                    elif event.key == pg.K_DOWN:
                        print("TODO impl down speed up") # TODO
                    elif event.key == pg.K_RIGHT:
                        self.falling_tetromino.shift(right=True);
                    elif event.key == pg.K_LEFT:
                        self.falling_tetromino.shift(right=False);

            # Update Logic
            self.falling_tetromino.fall();
            self.draw_screen();
            pg.display.flip();
            self.clock.tick(1);

    def draw_screen(self):
        self.screen.fill((0, 0, 0));
        # Draw all already placed blocks
        for row in range(20):
            row_empty = True;
            for cell in range(10):
                if self.game_array[19-row, cell]:
                    row_empty = False;
                    rect = (cell*self.block_size, row*self.block_size, self.block_size, self.block_size);
                    self.screen.fill((255, 255, 255), rect);
            # If row empty, nothing above
            if row_empty:
                break;

        # Draw falling tetromino as well
        tet = self.falling_tetromino;
        for row in range(4):
            board_y = (row + tet.offset.y) * self.block_size;
            for col in range(4):
                board_x = (col + tet.offset.x) * self.block_size;
                if tet.shape[row, col]:
                    rect = (board_x, board_y, self.block_size, self.block_size);
                    self.screen.fill((255, 255, 255), rect);

    def output_grid(self):
        output = np.copy(self.game_array);
        tetromino = self.falling_tetromino;
        cut_shape = np.copy(tetromino.shape);

        # Setup board bounds
        left_bound = int(tetromino.offset.x);
        right_bound = int(tetromino.offset.x + 3);
        top_bound = int(tetromino.offset.y);
        bottom_bound = int(tetromino.offset.y + 3); 

        # Remove oob from shape
        if left_bound < 0:
            cut_shape = cut_shape[:, abs(left_bound):4];
            left_bound = 0;
        elif right_bound > 9:
            cut_shape = cut_shape[:, 0:(4 - abs(9 - right_bound))];
            right_bound = 9;

        if top_bound < 0:
            cut_shape = cut_shape[abs(top_bound):4, :];
            top_bound = 0;
        elif bottom_bound > 19:
            cut_shape = cut_shape[0:(4 - abs(19 - bottom_bound)), :];
            bottom_bound = 19;

        # Account for exclusivity
        right_bound += 1;
        bottom_bound += 1;

        # Finally overwite
        # TODO change to draw on screen instead
        output[top_bound:bottom_bound, left_bound:right_bound] = cut_shape;
        print(output, '\n');
