"""Allows initialization and runtime of a Pytris game. 

Currently only allows creation and then playing. After calling play(),
game runs until it ends through user input. There are no other
external controls to stop or pause the game currently.
"""
import pygame as pg;
import numpy as np;
import random;
import tetromino;

class Pytris:
    """Used to play a Pytris game.

    Create with a board size (normal would be (10, 20),
    and then run with run(). Execution continues until the user
    presses the window quit button or quit key (ESCAPE).

    Controls:
        Left/Right Arrow: Move Tetromino left/right
        Up Arrow: Rotate Tetromino clockwise
        Down Arrow: Hold to increase fall speed by 3 times
        Space: Place Tetromino at ghost piece
        Left Shift: Hold current Tetromino
        Escape: Quit game
    """

    def __init__(self, board_size: pg.Vector2):
        """Creates a Pytris game with a specified board size.

        This sets up the variables needed for running the game.
        play() must be called after initialization to create game
        window and start main game loop.

        Args:
            board_size:
                Vector of board size. x and y are used to set size
                of board.

        Raises:
            ValueError: Board was not at least 4x4.
        """

        if (board_size.x < 4 or board_size.y < 4):
            raise ValueError("Board size must be at least 4x4");

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
        """Initializes graphics and input, and runs main game loop.

        Cannot be externally interrupted. Runs main loop until player 
        presses the window exit button, or the game exit key (ESCAPE).
        """
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
        """Main game loop.

        Checks and responds to user input, then executes game logic. 
        See main Pytris class documentation for inputs.
        Runs until user presses window exit button, or the escape button.
        """
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
            self.__draw_game_board();
            pg.display.update(self.__board_rect);

    ####################################
    # General Functions
    ####################################

    def __generate_tetromino(self) -> tetromino.Tetromino:
        """Instantiates a new Tetromino

        Uses a bucket method to ensure each type of piece is 
        generated exactly once before being repeated. 
        Once each type has been used, each one can be used
        once more, and so on.

        Returns:
            Tetromino: New random Tetromino instance.
        """
        if len(self.__bucket) == 0:
            self.__bucket = list(tetromino.TetrominoType);

        rand_type = random.choice(self.__bucket);
        self.__bucket.remove(rand_type);

        return tetromino.Tetromino(rand_type, self);

    def __get_next_tetromino(self) -> tetromino.Tetromino:
        """Removes and returns next Tetromino in queue

        Fills the queue with random Tetrominos, and returns the 
        next one in the queue. Returned Tetromino is removed 
        from queue.

        Returns:
            Tetromino: Next Tetromino in queue
        """
        while len(self.__tetromino_queue) <= self.__queue_size:
            self.__tetromino_queue.append(self.__generate_tetromino());
        next_tet = self.__tetromino_queue.pop(0);

        self.__draw_right_padding();
        return next_tet;

    def __place_tetromino(self):
        """Places falling Tetromino on board.

        Overwites the game board with the current falling Tetromino.
        Then replaces falling Tetromino with next in queue.
        """
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
        """Swaps falling Tetromino with held Tetromino.
        
        If another Tetromino is in hold, swaps with that one.
        If no Tetromino is in hold, puts Tetromino in hold,
        and sets the falling Tetromino to the next in queue.
        Can only be used once per block placed.
        """
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

    def __draw_game_board(self):
        """Updates game board graphics.
        
        Draws blocks on the graphical game_board. These include
        the game_board blocks, falling Tetromino blocks, and 
        falling Tetromino ghost blocks.
        """
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
        """Draws Tetromino on graphical game board.

        Uses information in passed Tetromino to draw on board. 

        Args:
            Tetromino:
                Tetromino to draw on board.
        """
        for row_index, row in enumerate(tetromino.shape):
            for col_index, block in enumerate(row):
                if block:
                    board_x = tetromino.offset.x + col_index;
                    board_y = tetromino.offset.y + row_index;
                    self.__draw_board_square(tetromino.color,
                                             self.__block_border_color, 
                                             pg.Vector2(board_x, board_y));

    def __draw_square(self, color: pg.Color, border_color: pg.Color, 
                      screen_pos: pg.Vector2, size: float):
        """Draws a square with a border on screen."""
        border_size = size / 20;
        outer_rect = pg.Rect(screen_pos.x, screen_pos.y,
                             size, size);
        inner_rect = pg.Rect(screen_pos.x + border_size, screen_pos.y + border_size,
                             size - (2*border_size), size - (2*border_size));

        self.__screen.fill(border_color, outer_rect);
        self.__screen.fill(color, inner_rect);
        
    def __draw_board_square(self, color: pg.Color, border_color: pg.Color, 
                            position: pg.Vector2):
        """Draws a square on the graphical game board.

        Args:
            position: Vector of game_board x and y index of block to draw 
        """
        screen_x = (position.x * self.__block_size) + self.__padding;
        screen_y = (position.y * self.__block_size);
        self.__draw_square(color, border_color, 
                           pg.Vector2(screen_x, screen_y), self.__block_size);

    def __draw_left_padding(self):
        """Draws left UI screen section.

        Draws the held block at the top center.
        """
        self.__screen.fill(self.__padding_color, self.__left_padding);

        if self.__held_tetromino != None:
            for row_index, row in enumerate(self.__held_tetromino.shape):
                for col_index, block in enumerate(row):
                    if block:
                        padding_block = self.__padding / 8;
                        tet_center = self.__held_tetromino.get_middle();

                        screen_x = 2 + col_index + (2 - tet_center.x);
                        screen_x *= padding_block;
                        screen_y = 2 + row_index + (2 - tet_center.y);
                        screen_y *= padding_block;

                        self.__draw_square(self.__held_tetromino.color,
                                           self.__padding_color,
                                           pg.Vector2(screen_x, screen_y),
                                           padding_block);

        pg.display.update(self.__left_padding);


    def __draw_right_padding(self):
        """Draws right UI screen section.

        Draws next in queue Tetrominos at the top center going down. 
        """
        self.__screen.fill(self.__padding_color, self.__right_padding);

        for tet_index, tet in enumerate(self.__tetromino_queue):
            for row_index, row in enumerate(tet.shape):
                for col_index, block in enumerate(row):
                    if block:
                        padding_block = self.__padding / 8;
                        tet_center = tet.get_middle();
                        screen_x = 2 + col_index + (2 - tet_center.x);
                        screen_x *= padding_block;
                        screen_x += self.__right_padding.x;
                        screen_y = 2 + row_index + (2 - tet_center.y);
                        screen_y += (5 * tet_index);
                        screen_y *= padding_block;
                        self.__draw_square(tet.color, self.__padding_color,
                                        pg.Vector2(screen_x, screen_y),
                                        padding_block);

        pg.display.update(self.__right_padding);

    ####################################
    # Getters
    ####################################

    @property
    def width(self) -> int:
        """Gets width of game_board array.
        
        Returns:
            int: width of game_board array.
        """
        return self.__width;

    @property
    def height(self) -> int:
        """Gets height of game_board array.

        Returns:
            int: height of game_board array.
        """
        return self.__height;
    
    @property
    def game_board(self) -> np.ndarray:
        """Gets a copy of the game_board array.

        Returns:
            ndarray: copy of game_board numpy array.
        """
        return np.copy(self.__game_board);

