import pygame as pg;
import numpy as np;
import random;
import tetromino;

class Pytris:
    def __init__(self, board_size: pg.Vector2):
        # Board setup
        self.__width = int(board_size.x);
        self.__height = int(board_size.y);
        self.__game_board = None;

        # PyGame / Graphics setup
        self.__background_color = pg.Color(25, 25, 25);
        self.__block_size = 30;
        self.__block_border_color = pg.Color(self.__background_color);
        self.__screen = None;
        self.__clock = None;

        # Misc setup
        self.__bucket = None;
        self.__falling_tetromino = None;
        self.__fps = 120;
        self.__fall_interval = 1000;
        self.__fall_counter = 0;
        self.__running = False;

    def play(self):
        if self.__running:
            return;

        empty_board = [[None for col in range(self.__width)] for row in range(self.__height)]; 
        self.__game_board = np.array(empty_board);
        self.__bucket = list(tetromino.TetrominoType);
        self.__falling_tetromino = self.__generate_tetromino();
        self.__fall_interval = 1000;

        pg.init();
        self.__screen = pg.display.set_mode([
            self.__width*self.__block_size,
            self.__height*self.__block_size]);
        self.__clock = pg.time.Clock();

        self.__running = True
        self.__play();
        pg.quit();

    def __play(self):
        while self.__running:
            # Input reading
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False;
                    return;
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.__falling_tetromino.rotate(right=True);
                    elif event.key == pg.K_DOWN:
                        self.__fall_interval /= 3;
                    elif event.key == pg.K_RIGHT:
                        self.__falling_tetromino.shift(right=True);
                    elif event.key == pg.K_LEFT:
                        self.__falling_tetromino.shift(right=False);
                    elif event.key == pg.K_SPACE:
                        while self.__falling_tetromino.fall():
                            pass;
                        self.__place_tetromino();
                    elif event.key == pg.K_ESCAPE:
                        self.__running = False;
                        return;
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        self.__fall_interval *= 3;

            # Update speed_counter
            self.__fall_counter += self.__clock.tick(self.__fps);
            if self.__fall_counter >= self.__fall_interval:
                self.__fall_counter -= self.__fall_interval;
                if not self.__falling_tetromino.fall():
                    self.__place_tetromino();

            # Update display
            self.__draw_screen();
            pg.display.flip();

    def __generate_tetromino(self) -> tetromino.Tetromino:
        if len(self.__bucket) == 0:
            self.__bucket = list(tetromino.TetrominoType);

        rand_type = random.choice(self.__bucket);
        self.__bucket.remove(rand_type);

        return tetromino.Tetromino(rand_type, self);

    def __draw_screen(self):
        self.__screen.fill(self.__background_color);

        # Draw all already placed blocks
        for row_index, row in enumerate(self.__game_board):
            for col_index, cell in enumerate(row):
                if cell:
                    rect = pg.Rect(col_index*self.__block_size, 
                                   row_index*self.__block_size,
                                   self.__block_size, self.__block_size);
                    self.__draw_border_square(cell, rect);

        # Draw falling tetromino as well
        tet = self.__falling_tetromino;
        for row_index, row in enumerate(tet.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    board_x = tet.offset.x + col_index;
                    board_y = tet.offset.y + row_index;
                    board_x *= self.__block_size;
                    board_y *= self.__block_size;
                    rect = pg.Rect(board_x, board_y,
                                   self.__block_size, self.__block_size);
                    self.__draw_border_square(tet.color, rect);

    def __draw_border_square(self, color: pg.Color, rect: pg.Rect):
        thick = self.__block_size / 20;
        inner_rect = pg.Rect.copy(rect);
        inner_rect.x += thick;
        inner_rect.y += thick;
        inner_rect.width -= (2*thick);
        inner_rect.height -= (2*thick);

        self.__screen.fill(self.__block_border_color, rect);
        self.__screen.fill(color, inner_rect);

    def __place_tetromino(self):
        tet = self.__falling_tetromino;
        for row_index, row in enumerate(tet.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    board_x = tet.offset.x + col_index;
                    board_y = tet.offset.y + row_index;
                    self.__game_board[int(board_y), int(board_x)] = tet.color;

        self.__check_board();
        self.__falling_tetromino = self.__generate_tetromino();
        self.__fall_counter = 0;

    def __check_board(self):
        for row_index, row in enumerate(self.__game_board):
            if np.all(row != None):
                self.__game_board[1:row_index+1, :] = self.__game_board[0:row_index, :];
                self.__game_board[0, :] = None;

    ####################################
    # Getters
    ####################################

    @property
    def width(self):
        return self.__width;

    @property
    def height(self):
        return self.__height;
    
    @property
    def game_board(self):
        return np.copy(self.__game_board);

