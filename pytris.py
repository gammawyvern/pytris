import pygame as pg;
import random;
from pygame import Vector2;
from tetromino import Tetromino, TetrominoType;
import numpy as np;

class Pytris:
    def __init__(self):
        pg.init();
        self.screen = pg.display.set_mode([300, 600]);
        self.clock = pg.time.Clock();

        self.falling_tetromino = None;
        self.fps = 120;
        self.fall_speed = 1000;
        self.fall_counter = 0;
        self.running = True;

        # Screen/Draw info
        self.game_array = np.zeros((20, 10));
        self.block_size = 30;

        self.__setup();
        self.__play();
        pg.quit();

    def __setup(self):
        self.falling_tetromino = self.__generate_tetromino();

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

            # Update counter from delta time
            self.fall_counter += self.clock.tick(60);

            # Update based on speed
            collision = False;
            if self.fall_counter >= self.fall_speed:
                collision = not self.falling_tetromino.fall();
                self.fall_counter -= self.fall_speed;
            if collision:
                self.__place_tetromino();
                pass;

            # Update Logic
            self.draw_screen();
            pg.display.flip();

    def __generate_tetromino(self) -> Tetromino:
        # TODO implement bucket randomness
        rand_type = random.choice(list(TetrominoType));
        return Tetromino(rand_type);

    def draw_screen(self):
        self.screen.fill((0, 0, 0));
        # Draw all already placed blocks
        for row in range(19, -1, -1):
            row_empty = True;
            for cell in range(10):
                if self.game_array[row, cell]:
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

    def __place_tetromino(self):
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

        self.game_array[top_bound:bottom_bound, left_bound:right_bound] = cut_shape;
        print(self.game_array);
        self.falling_tetromino = self.__generate_tetromino();
