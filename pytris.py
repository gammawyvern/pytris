import pygame as pg;
from pygame import Vector2;
from tetromino import Tetromino, TetrominoType;
import numpy as np;

class Pytris:
    def __init__(self):
        pg.init();
        self.screen = pg.display.set_mode([300, 600]);
        self.clock = pg.time.Clock();

        self.game_array = np.zeros((20, 10));
        self.falling_tetromino = None;
        self.running = True;

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
            pg.display.flip();
            self.output_grid();
            self.clock.tick(1);

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
