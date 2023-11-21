import pygame as pg;
import numpy as np;
import random;
import tetromino;

class Pytris:
    def __init__(self, board_size: pg.Vector2):
        # Board setup
        self.width = int(board_size.x);
        self.height = int(board_size.y);
        self.game_board = np.full((self.height, self.width), None, dtype=tuple);

        # PyGame / Graphics setup
        pg.init();
        self.background_color = (25, 25, 25);
        self.block_size = 30;
        # I like how it looks with just gaps between blocks
        self.block_border_color = self.background_color;
        self.screen = pg.display.set_mode([
            self.block_size*self.width,
            self.block_size*self.height]);
        self.clock = pg.time.Clock();

        # Misc setup
        self.bucket = list(tetromino.TetrominoType);
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
                        while self.falling_tetromino.fall():
                            pass;
                        self.__place_tetromino();
                    elif event.key == pg.K_ESCAPE:
                        self.running = False;
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        self.fall_speed *= 3;

            # Update counter from delta time
            self.fall_counter += self.clock.tick(60);

            # Update based on speed
            if self.fall_counter >= self.fall_speed:
                self.fall_counter -= self.fall_speed;
                if not self.falling_tetromino.fall():
                    self.__place_tetromino();

            # Update Logic
            self.draw_screen();
            pg.display.flip();

    def __generate_tetromino(self) -> tetromino.Tetromino:
        if len(self.bucket) == 0:
            self.bucket = list(tetromino.TetrominoType);

        rand_type = random.choice(self.bucket);
        self.bucket.remove(rand_type);

        return tetromino.Tetromino(rand_type, self);

    def draw_screen(self):
        self.screen.fill(self.background_color);

        # Draw all already placed blocks
        for row in range(self.height):
            for col in range(self.width):
                if self.game_board[row, col]:
                    rect = (col*self.block_size, row*self.block_size, self.block_size, self.block_size);
                    self.__draw_border_square(self.game_board[row, col], rect);

        # Draw falling tetromino as well
        tet = self.falling_tetromino;
        for row in range(4):
            board_y = tet.offset.y + row;
            board_y *= self.block_size;
            for col in range(4):
                board_x = tet.offset.x + col;
                board_x *= self.block_size;
                
                if tet.shape[row, col]:
                    rect = (board_x, board_y, self.block_size, self.block_size);
                    self.__draw_border_square(tet.color, rect);

    # Draws square with border
    def __draw_border_square(self, color, rect):
        thick = self.block_size / 20;
        inner_rect = (rect[0]+thick, rect[1]+thick, rect[2]-(2*thick), rect[3]-(2*thick));
        self.screen.fill(self.block_border_color, rect);
        self.screen.fill(color, inner_rect);

    def __place_tetromino(self):
        tet = self.falling_tetromino;
        for row in range(4):
            board_y = tet.offset.y + row;
            for col in range(4):
                board_x = tet.offset.x + col;
                if tet.shape[row, col]:
                    self.game_board[int(board_y), int(board_x)] = tet.color;

        self.__check_board();
        self.falling_tetromino = self.__generate_tetromino();
        self.fall_counter = 0;

    def __check_board(self):
        for row in range(self.height):
            if np.all(self.game_board[row] != None):
                self.game_board[1:row+1, :] = self.game_board[0:row, :];
                self.game_board[0, :] = None;

