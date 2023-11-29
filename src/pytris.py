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
        self.__background_color = pg.Color(35, 35, 35);
        self.__block_size = 32;
        self.__padding = 4 * self.__block_size;
        self.__padding_color = pg.Color(20, 20, 20);
        self.__block_border_color = pg.Color(self.__background_color);
        self.__board_rect = pg.Rect(self.__padding, 0,
                                    self.__block_size*self.__width,
                                    self.__block_size*self.__height);
        self.__left_padding = pg.Rect(0, 0,
                                      self.__padding, self.__board_rect.height);
        self.__right_padding = pg.Rect(self.__padding + self.__board_rect.width, 0,
                                       self.__padding, self.__board_rect.height);
        self.__screen = None;
        self.__clock = None;

        # Misc setup
        self.__bucket = None;
        self.__queue_size = 3;
        self.__falling_tetromino = None;
        self.__held_tetromino = None;
        self.__can_hold = True;
        self.__tetromino_queue = [];
        self.__fps = 120;
        self.__fall_interval = 1000;
        self.__fall_counter = 0;
        self.__running = False;

    ####################################
    # Setup Function
    ####################################

    def play(self):
        if self.__running:
            return;

        empty_board = [[None for _ in range(self.__width)] for _ in range(self.__height)]; 
        self.__game_board = np.array(empty_board);
        self.__bucket = list(tetromino.TetrominoType);
        self.__fall_interval = 1000;

        pg.init();
        self.__screen = pg.display.set_mode([
            (self.__padding + self.__board_rect.width + self.__padding),
            (self.__board_rect.height)]);
        self.__screen.fill(self.__padding_color);
        pg.display.flip();
        self.__clock = pg.time.Clock();

        self.__falling_tetromino = self.__get_next_tetromino();

        self.__running = True
        self.__play();
        pg.quit();

    ####################################
    # Main Gameplay Loop Function
    ####################################

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
                        self.__fall_counter /= 3;
                    elif event.key == pg.K_RIGHT:
                        self.__falling_tetromino.shift(right=True);
                    elif event.key == pg.K_LEFT:
                        self.__falling_tetromino.shift(right=False);
                    elif event.key == pg.K_SPACE:
                        while self.__falling_tetromino.fall():
                            pass;
                        self.__place_tetromino();
                    elif event.key == pg.K_LSHIFT:
                        self.__hold_tetromino();
                    elif event.key == pg.K_ESCAPE:
                        self.__running = False;
                        return;
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        self.__fall_interval *= 3;
                        self.__fall_counter *= 3;

            # Update speed_counter
            self.__fall_counter += self.__clock.tick(self.__fps);
            if self.__fall_counter >= self.__fall_interval:
                self.__fall_counter -= self.__fall_interval;
                if not self.__falling_tetromino.fall():
                    self.__place_tetromino();

            # Update display
            self.__draw_screen();
            pg.display.update(self.__board_rect);

    ####################################
    # General Functions
    ####################################

    def __generate_tetromino(self) -> tetromino.Tetromino:
        if len(self.__bucket) == 0:
            self.__bucket = list(tetromino.TetrominoType);

        rand_type = random.choice(self.__bucket);
        self.__bucket.remove(rand_type);

        return tetromino.Tetromino(rand_type, self);

    def __get_next_tetromino(self) -> tetromino.Tetromino:
        while len(self.__tetromino_queue) <= self.__queue_size:
            self.__tetromino_queue.append(self.__generate_tetromino());
        next_tet = self.__tetromino_queue.pop(0);

        self.__draw_right_padding();
        return next_tet;

    def __place_tetromino(self):
        tet = self.__falling_tetromino;
        for row_index, row in enumerate(tet.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    board_x = tet.offset.x + col_index;
                    board_y = tet.offset.y + row_index;
                    self.__game_board[int(board_y), int(board_x)] = tet.color;

        self.__clear_full_rows();
        self.__falling_tetromino = self.__get_next_tetromino();
        self.__fall_counter = 0;
        self.__can_hold = True;

    def __hold_tetromino(self):
        if not self.__can_hold:
            return;

        if self.__held_tetromino == None:
            self.__held_tetromino = self.__falling_tetromino;
            self.__falling_tetromino = self.__get_next_tetromino(); 
        else:
            self.__falling_tetromino.reset();
            temp_tetromino = self.__held_tetromino;
            self.__held_tetromino = self.__falling_tetromino;
            self.__falling_tetromino = temp_tetromino;

        self.__draw_left_padding();
        self.__fall_counter = 0;
        self.__can_hold = False;

    def __clear_full_rows(self):
        for row_index, row in enumerate(self.__game_board):
            if np.all(row != None):
                self.__game_board[1:row_index+1, :] = self.__game_board[0:row_index, :];
                self.__game_board[0, :] = None;

    ####################################
    # Drawing functions
    ####################################

    def __draw_screen(self):
        self.__screen.fill(self.__background_color, self.__board_rect);

        # Draw all already placed blocks
        for row_index, row in enumerate(self.__game_board):
            for col_index, block in enumerate(row):
                if block:
                    self.__draw_board_square(block, self.__block_border_color, 
                                             pg.Vector2(col_index, row_index));

        # Draw other tetrominos
        self.__draw_tetromino(self.__falling_tetromino.get_ghost());
        self.__draw_tetromino(self.__falling_tetromino);

    def __draw_tetromino(self, tetromino):
        for row_index, row in enumerate(tetromino.shape):
            for col_index, block in enumerate(row):
                if block:
                    board_x = tetromino.offset.x + col_index;
                    board_y = tetromino.offset.y + row_index;
                    pos = pg.Vector2(board_x, board_y);
                    self.__draw_board_square(tetromino.color,
                                             self.__block_border_color, 
                                             pos);

    def __draw_square(self, color: pg.Color, border_color: pg.Color, 
                      board_pos: pg.Vector2, size: float):
        border_size = size / 20;
        outer_rect = pg.Rect(board_pos.x, board_pos.y,
                             size, size);
        inner_rect = pg.Rect(board_pos.x + border_size, board_pos.y + border_size,
                             size - (2*border_size), size - (2*border_size));

        self.__screen.fill(border_color, outer_rect);
        self.__screen.fill(color, inner_rect);
        
    def __draw_board_square(self, color: pg.Color, border_color: pg.Color, 
                            position: pg.Vector2):
        screen_x = (position.x * self.__block_size) + self.__padding;
        screen_y = (position.y * self.__block_size);
        self.__draw_square(color, border_color, 
                           pg.Vector2(screen_x, screen_y), self.__block_size);

    def __draw_left_padding(self):
        self.__screen.fill(self.__padding_color, self.__left_padding);

        if self.__held_tetromino != None:
            for row_index, row in enumerate(self.__held_tetromino.shape):
                for col_index, block in enumerate(row):
                    if block:
                        padding_block = self.__padding / 8;
                        screen_x = (self.__padding / 2) - (2 * padding_block);
                        screen_x += (padding_block * col_index);
                        screen_y = (2 * padding_block) + (padding_block * row_index);
                        self.__draw_square(self.__held_tetromino.color,
                                           self.__padding_color,
                                           pg.Vector2(screen_x, screen_y),
                                           padding_block);

        pg.display.update(self.__left_padding);


    def __draw_right_padding(self):
        self.__screen.fill(self.__padding_color, self.__right_padding);

        for tet_index, tet in enumerate(self.__tetromino_queue):
            for row_index, row in enumerate(tet.shape):
                for col_index, block in enumerate(row):
                    if block:
                        padding_block = self.__padding / 8;
                        screen_x = self.__right_padding.x + (self.__padding / 2) - (2 * padding_block) 
                        screen_x += (padding_block * col_index);
                        screen_y = (2 * padding_block) + (padding_block * row_index);
                        screen_y += (5 * padding_block * tet_index);
                        self.__draw_square(tet.color, self.__padding_color,
                                        pg.Vector2(screen_x, screen_y),
                                        padding_block);

        pg.display.update(self.__right_padding);

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

