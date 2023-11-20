import pygame as pg;
import random;
from pygame import Vector2;
from tetromino import Tetromino, TetrominoType;
import numpy as np;

class Pytris:
    def __init__(self, board_size: Vector2):
        # Board setup
        self.width = int(board_size.x);
        self.height = int(board_size.y);
        self.game_board = np.zeros((self.height, self.width));

        # PyGame / Graphics setup
        pg.init();
        self.block_size = 30;
        self.screen = pg.display.set_mode([
            self.block_size*self.width,
            self.block_size*self.height]);
        self.clock = pg.time.Clock();

        # Misc setup
        self.falling_tetromino = self.__generate_tetromino();
        self.fps = 120;
        self.fall_speed = 1000;
        self.fall_counter = 0;
        self.running = True;

        self.__play();
        pg.quit();

    def __play(self):
        while self.running:
            # Input reading
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False;
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.falling_tetromino.rotate();
                    elif event.key == pg.K_DOWN:
                        self.fall_speed /= 3;
                    elif event.key == pg.K_RIGHT:
                        self.falling_tetromino.shift(right=True);
                    elif event.key == pg.K_LEFT:
                        self.falling_tetromino.shift(right=False);
                    elif event.key == pg.K_SPACE:
                        self.__place_tetromino();
                    elif event.key == pg.K_ESCAPE:
                        self.running = False;
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        self.fall_speed *= 3;

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
        return Tetromino(rand_type, self);

    def draw_screen(self):
        self.screen.fill((0, 0, 0));

        # Draw all already placed blocks
        for row in range(self.height):
            for col in range(self.width):
                if self.game_board[row, col]:
                    rect = (col*self.block_size, row*self.block_size, self.block_size, self.block_size);
                    self.screen.fill((255, 255, 255), rect);

        # Draw falling tetromino as well
        tet = self.falling_tetromino;
        for row in range(4):
            board_y = (tet.offset.y + row) % self.height;
            board_y *= self.block_size;
            for col in range(4):
                board_x = (tet.offset.x + col) % self.width;
                board_x *= self.block_size;
                
                if tet.shape[row, col]:
                    rect = (board_x, board_y, self.block_size, self.block_size);
                    self.screen.fill((255, 255, 255), rect);

    def __place_tetromino(self):
        tet = self.falling_tetromino;
        for row in range(4):
            board_y = (tet.offset.y + row) % self.height;
            for col in range(4):
                board_x = (tet.offset.x + col) % self.width;
                
                if tet.shape[row, col]:
                    self.game_board[int(board_y), int(board_x)] = 1;

        self.__check_board();
        self.falling_tetromino = self.__generate_tetromino();

    def __check_board(self):
        for row in range(self.height):
            if np.all(self.game_board[row] == 1):
                # TODO this may break at the very top row????
                self.game_board[1:row+1, :] = self.game_board[0:row, :];
                self.game_board[0, :] = 0;

